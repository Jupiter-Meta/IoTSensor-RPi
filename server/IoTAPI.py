from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz

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

@app.route('/data')
def get_data():
    # Query MongoDB for the last 3 records
    data = list(collection.find().sort("_id", -1).limit(3))
    
    # Convert epoch timestamps to IST
    ist = pytz.timezone('Asia/Kolkata')
    data_list = []
    for record in data:
        timestamp_utc = datetime.utcfromtimestamp(record["fetchtime"])
        timestamp_ist = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(ist)
        
        data_list.append({
            "temperature": record["temperature"],
            "humidity": record["humidity"],
            "timestamp": timestamp_ist.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            "timestamp_epoch": record["fetchtime"],
            "lat": record["lat"],
            "lon": record["lon"]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051, debug=True)
