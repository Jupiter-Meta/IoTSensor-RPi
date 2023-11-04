import Adafruit_DHT
import paho.mqtt.client as mqtt
import json, geocoder
import time
from lightsensorRead import readLight
import mh_z19

#read light sensor
try:
  lightlevel = readLight()
except:
  lightlevel = -1.0
#light sensor value is -1 if there is sensor error

#read CO2 level
try:
  co2 = mh_z19.read()
  co2 = co2['co2']
except:
  co2 = -1

data = {'lightlevel':lightlevel, 'co2':co2}
print(data)
