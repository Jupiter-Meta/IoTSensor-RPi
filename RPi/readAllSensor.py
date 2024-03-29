import Adafruit_DHT
import paho.mqtt.client as mqtt
import json, geocoder
import time, socket, psutil
from lightsensorRead import readLight
import mh_z19
import board, geocoder
import sds011
from mqtthelper import publish
from getaqi import calculate_overall_aqi
print("Reading Sensor Value")

def get_interface_ip(interface_name):
    try:
        addresses = psutil.net_if_addrs()
        # print(addresses)
        if interface_name in addresses:
            for address in addresses[interface_name]:
                if address.family == socket.AF_INET:
                    return address.address
    except Exception as e:
        return str(e)
    
    return "Not found"

hostname = socket.gethostname()

eth0_ip = get_interface_ip("eth0")
wifi_ip = get_interface_ip("wlan0")

#Read PM2.5 and PM10    
try:
    sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
    sensor.sleep(sleep=0)
except:
    PM = [-1, -1]

#Connect and wakeup PM Sensor
# sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=True)
# sensor.sleep(sleep=0)

#get lat and long
location = geocoder.ip('me')
if location.ok:
    latitude = location.latlng[0]
    longitude = location.latlng[1]
else:
    latitude = 0.0
    longitude = 0.0


#read light sensor
try:
  lightlevel = round(readLight(),2)
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
  temperatureco2 = -1

#Read DHT11
try:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 17)
except:
    humidity = -1
    temperature = -1

#read PM 2.5 and PM10
try:
    PM = sensor.query()
    sensor.sleep()

except:
    print("error2")
    PM = [-2, -2]
#get AQI values
try:
    aqi = calculate_overall_aqi(PM[0], PM[1], co2)
except:
    aqi = -1

data = {
    'devicename':hostname,
    'eth0_ip':eth0_ip,
    'wifi_ip':wifi_ip, 
    'lightlevel':lightlevel,
    'co2':co2,
    'temperatureco2':temperatureco2,
    'pm2_5':PM[0],
    'pm10':PM[1],
    'temperature': temperature,
    'humidity': humidity,
    'aqi': aqi,
    'fetchtime': int(time.time()),
    'lat':latitude,
    'lon':longitude
}
print(data)
publish("65.2.135.170","JM/ALLSENSOR",data)
print("Published to AWS")
# publish("192.168.1.109","JM/ALLSENSOR",data)
# print("Published to Local Edge Node")
