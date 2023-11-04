import adafruit_dht
import paho.mqtt.client as mqtt
import json, geocoder
import time
from lightsensorRead import readLight
import mh_z19
import board
from sds011reader import SDS011Reader


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
  print(co2Sensor)
except:
  co2 = -1
  temperatureco2 = -1

#Read DHT11
try:
  dhtDevice = adafruit_dht.DHT11(board.D17)
  humidity = dhtDevice.humidity
  temperature = dhtDevice.temperature
except:
  humidity = -1
  temperature = -1

#Read PM2.5 and PM10    
try:
  AQIsensor = SDS011Reader()
  AQIsensor.sensor_wake()
  PM = AQIsensor.readValue()
  AQIsensor.sensor_sleep()
  AQIsensor.close()
except:
  PM = [-1, -1]

data = {
  'lightlevel':lightlevel,
  'co2':co2,
  'temperatureco2':temperatureco2,
  'pm2_5':PM[0],
  'pm10':PM[1],
  'temperature': temperature,
  'humidity': humidity,
  'fetchtime': int(time.time()),
  'lat':0,
  'lon':0
}
print(data)
