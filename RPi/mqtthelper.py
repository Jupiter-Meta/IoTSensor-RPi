import paho.mqtt.client as mqtt
import json

MQTT_BROKER_HOST = "65.2.135.170"
MQTT_BROKER_PORT = 1883
# MQTT_TOPIC = "JM/ALLSENSOR"

client = mqtt.Client()

def publish(MQTT_TOPIC, data):
  
  client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
  client.publish(MQTT_TOPIC, json.dumps(data))
  client.disconnect()
