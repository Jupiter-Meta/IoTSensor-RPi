import Adafruit_DHT
import paho.mqtt.client as mqtt
import json, geocoder
import time
from lightsensorRead import readLight
import mh_z19
# from 



#read light sensor
try:
  lightlevel = round(readLight())
except:
  lightlevel = -1.0
#light sensor value is -1 if there is sensor error

#read CO2 level
try:
  co2Sensor = mh_z19.read_all()
  co2 = co2Sensor['co2']
  temperatureco2 = co2Sensor['temperature']
except:
  co2 = -1

#Read DHT11
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17 # Replace with the actual GPIO pin number

try:
  humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
  print(humidity)
  print(temperature)
  if humidity is not None and temperature is not None:
    humidity = -1
    temperature = -1
except:
  humidity = -1
  temperature = -1
    
    

data = {
  'lightlevel':lightlevel,
  'co2':co2,
  'temperatureco2':temperatureco2,
  'pm2_5':0,
  'pm10':0,
  'temperature': temperature,
  'humidity': humidity,
  'fetchtime': int(time.time()),
  'lat':0,
  'lon':0
}
print(data)
