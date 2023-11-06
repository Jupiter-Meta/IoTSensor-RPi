from sds011 import SDS011
import time

# Replace 'COMx' with the actual COM port number (e.g., 'COM3')
port = "'dev/ttyUSB0"  # Encode the port name as bytes

def read_sds011_sensor(port):
    try:
        sds = SDS011(port=port)
        sds.set_work_period(work_time=0)  # Set continuous mode

        while True:
            pm25, pm10 = sds.query()
            print(f'PM2.5: {pm25} µg/m³, PM10: {pm10} µg/m³')

            # Put the sensor to sleep and turn off the fan
            sds.set_sleep(sleep=True)

            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        # Set to sleep mode and turn off the fan before exiting
        sds.set_sleep(sleep=True)
        print('Exiting.')

if __name__ == "__main__":
    read_sds011_sensor(port)
