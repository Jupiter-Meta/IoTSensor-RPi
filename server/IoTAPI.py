from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz,json

app = Flask(__name__)

# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jm"
MONGO_COLLECTION = "IoTSensorData"

# MongoDB connection setup
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]
print(mongo_client)

@app.route('/')
def welcome():
    return "welcome"

@app.route('/data/<val>')
def get_data(val):
    # Query MongoDB for the last 3 records
    data = list(collection.find().sort("_id", -1).limit(int(val)))
    print(data)
    #Convert epoch timestamps to IST
    ist = pytz.timezone('Asia/Kolkata')
    data_list = []
    for record in data:
        timestamp_utc = datetime.utcfromtimestamp(record["fetchtime"])
        timestamp_ist = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(ist)
        
        data_list.append({
            "timestamp": timestamp_ist.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            "timestamp_epoch": record["fetchtime"],
            "lightlevel":record["lightlevel"],
            "lat":record["lat"],
            "lon":record["lon"],
            "co2":record["co2"],
            "temperatureco2":record["temperatureco2"],
            "pm2_5":record["pm2_5"],
            "pm10":record["pm10"],
            "temperature":record["temperature"],
            "humidity":record["humidity"]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051, debug=True)
