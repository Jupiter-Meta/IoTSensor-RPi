#!/usr/bin/python3
import sys
import os
import paho.mqtt.client as paho
import json
import ast
from datetime import datetime
from pymongo import MongoClient



global mqttclient;
global broker;
global port;

# Define MQTT information
broker = "0.0.0.0";
port = 1883;
mypid = os.getpid()
print("Process started at: " +str(mypid))
client_uniq = "pubclient_"+str(mypid)
mqttclient = paho.Client(client_uniq, True) #nocleanstart

# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jm"

def on_log(buf):
	print("log:",buf)
# 	print(client)
# 	print(userdata)
# 	print(level)
	mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
	db = mongo_client[MONGO_DB]
	MONGO_COLLECTION = "MQTTLog"
	collection.insert_one(buf)
	mongo_client.close()



def test(client, userdata, message):
	print("Test Channel")
	print("Received message '" + str(message.payload.decode()) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
	mqttData={'message':str(message.payload.decode()),'topic':message.topic,'qos':str(message.qos)}
	mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
	db = mongo_client[MONGO_DB]
	MONGO_COLLECTION = "MQTTTest"
	collection = db[MONGO_COLLECTION]
	collection.insert_one(mqttData)
	mongo_client.close()
	print("DB DUMP suceess for MQTT Test")
	
def allSensors(client, userdata, msg):
	
	try:
		data = json.loads(msg.payload.decode())
		mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
		db = mongo_client[MONGO_DB]
		MONGO_COLLECTION = "iotsensordatas"
		collection = db[MONGO_COLLECTION]
		collection.insert_one(data)
		print("Data inserted into MongoDB:")
		print(data)
		mongo_client.close()
	except Exception as e:
		print(f"Error: {str(e)}")

def doorSensor(client, userdata, msg):

	try:
        # Decode the received JSON message
		data = json.loads(msg.payload.decode())
        
        # Connect to MongoDB
		mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
		db = mongo_client[MONGO_DB]
		MONGO_COLLECTION = "ConferenceRoomAccess"
		collection = db[MONGO_COLLECTION]
        
        # Insert the JSON data into MongoDB
		collection.insert_one(data)
		print("Data inserted into MongoDB:")
		print(data)
        
        # Disconnect from MongoDB
		mongo_client.close()
	except Exception as e:
		print(f"Error: {str(e)}")

def dht(client, userdata, msg):

	try:
        # Decode the received JSON message
		data = json.loads(msg.payload.decode())
        
        # Connect to MongoDB
		mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
		db = mongo_client[MONGO_DB]
		MONGO_COLLECTION = "conferenceroomdht"
		collection = db[MONGO_COLLECTION]
        
        # Insert the JSON data into MongoDB
		collection.insert_one(data)
		print("Data inserted into MongoDB:")
		print(data)
        
        # Disconnect from MongoDB
		mongo_client.close()
	except Exception as e:
		print(f"Error: {str(e)}")



	
def _on_message(client, userdata, msg):
# 	print("Received: Topic: %s Body: %s", msg.topic, msg.payload)
	print(msg.topic+" "+str(msg.payload))
	 
#Subscribed Topics 
def _on_connect(mqttclient, userdata, flags, rc):
# 	print("New Client: "+str(mqttclient)+ " connected")
# 	print(rc)
	mqttclient.subscribe("JM/#", qos=0)	
	

mqttclient.message_callback_add("JM/TEST", test)
mqttclient.message_callback_add("JM/ALLSENSOR", allSensors)
# mqttclient.message_callback_add("JM/DOORSENSOR", doorSensor)
mqttclient.message_callback_add("JM/sensor1", doorSensor)
mqttclient.message_callback_add("JM/DHT", dht)
	      
mqttclient.connect(broker, port, keepalive=1, bind_address="")
  
mqttclient.on_log=on_log # set client logging	
mqttclient.on_connect = _on_connect   
mqttclient.loop_forever()


