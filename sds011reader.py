import os
import serial
import time
import datetime
import sys
import numpy as np

class SDS011Reader:
    """This is a wrapper for the implimentation from ronanj"""

    def __init__(self, inport = "/dev/ttyUSB0"):
        self.serial = serial.Serial(port=inport,baudrate=9600)

    def readValue( self ):
        step = 0
        while True: 
            while self.serial.inWaiting()!=0:
                v=ord(self.serial.read())

                if step ==0:
                    if v==170:
                        step=1

                elif step==1:
                    if v==192:
                        values = [0,0,0,0,0,0,0]
                        step=2
                    else:
                        step=0

                elif step>8:
                    step =0
                    pm25 = float(values[0]+values[1]*256)/10 #divided by 10 to get correct values
                    pm10 = float(values[2]+values[3]*256)/10
                    return [pm25,pm10]

                elif step>=2:
                    values[step-2]=v
                    step= step+1



    def read( self, duration ):
        start = os.times()[4]

        count = 0
        species = [[],[]]
        speciesType = ["pm2.5-mg","pm10-mg"]

        while os.times()[4]<start+duration:
            try:
                values = self.readValue()
                species[0].append(values[0])
                species[1].append(values[1])
                count += 1
                dt = os.times()[4]-start
                print("[{:4.1f}] Samples:{:2d} PM2.5:{:4d} PM10:{:4d} StdDev(PM2.5):{:3.1f}".format(
                    dt,count,values[0],values[1],np.std(species[0])
                    ))
                time.sleep(1)
            except KeyboardInterrupt:
                print("Bye")
                sys.exit()
            except:
                e = sys.exc_info()[0]
                print("Can not read the sensor data: "+str(e))

        values = []
        for i in range(len(species)):
            values.append( dict( 
                stddev = np.std(species[i]), 
                median = np.median(species[i]),
                min    = np.min(species[i]),
                max    = np.max(species[i]),
                avg    = np.average(species[i]),
                type   = speciesType[i],
                time   = datetime.now().isoformat(),
                sensor = "SDS",
                scale  = 1
                ))

        return values
    
    def close(self):
        self.serial.close()

    def sensor_wake(self):
        bytes = ['\xaa', #head
        '\xb4', #command 1
        '\x06', #data byte 1
        '\x01', #data byte 2 (set mode)
        '\x01', #data byte 3 (sleep)
        '\x00', #data byte 4
        '\x00', #data byte 5
        '\x00', #data byte 6
        '\x00', #data byte 7
        '\x00', #data byte 8
        '\x00', #data byte 9
        '\x00', #data byte 10
        '\x00', #data byte 11
        '\x00', #data byte 12
        '\x00', #data byte 13
        '\xff', #data byte 14 (device id byte 1)
        '\xff', #data byte 15 (device id byte 2)
        '\x05', #checksum
        '\xab'] #tail
        for b in bytes:
            self.serial.write(b.encode())
