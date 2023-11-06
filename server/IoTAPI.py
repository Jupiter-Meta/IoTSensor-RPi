from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz,json,sys
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jm"
# MONGO_COLLECTION = "IoTSensorData"

# MongoDB connection setup
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo_client[MONGO_DB]

def security(fname):
	APILog={'clientAgent':str(request.headers.get('User-Agent')),
		'clientIP':str(request.environ['REMOTE_ADDR']),
		'API':fname}
	MONGO_COLLECTION = "APILOG"
	collection = db[MONGO_COLLECTION]
	collection.insert_one(APILog)
    

@app.route('/')
def welcome():
	security(str(sys._getframe().f_code.co_name))
	return "welcome"

@app.route('/data/<val>')
def get_IoT_data(val):
    MONGO_COLLECTION = "IoTSensorData"
    security(str(sys._getframe().f_code.co_name))
    collection = db[MONGO_COLLECTION]
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
            "aqi":record["aqi"],
            "temperatureco2":record["temperatureco2"],
            "pm2_5":record["pm2_5"],
            "pm10":record["pm10"],
            "temperature":record["temperature"],
            "humidity":record["humidity"]
        })

    return jsonify(data_list)

@app.route('/weather/<val>')
def get_Weather_data(val):
    security(str(sys._getframe().f_code.co_name))
    MONGO_COLLECTION = "weatherKL"
    collection = db[MONGO_COLLECTION]
    # Query MongoDB for the last 3 records
    data = list(collection.find().sort("_id", -1).limit(int(val)))
    print(data)
    #Convert epoch timestamps to IST
    ist = pytz.timezone('Asia/Kolkata')
    data_list = []
    for record in data:
        timestamp_utcFT = datetime.utcfromtimestamp(record["fetchTime"])
        timestamp_istFT = timestamp_utcFT.replace(tzinfo=pytz.utc).astimezone(ist)
        
        timestamp_utcUT = datetime.utcfromtimestamp(record["lastUpdate"])
        timestamp_istUT = timestamp_utcUT.replace(tzinfo=pytz.utc).astimezone(ist)
        
        data_list.append({
            "timestamp": timestamp_istFT.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            "timestamp_epoch": record["fetchTime"],
            "lastUpdate": timestamp_utcUT.strftime('%Y-%m-%d %H:%M:%S %Z%z'),
            "lastUpdate_epoch": record["lastUpdate"],         
            "lat": record["lat"],
            "lon": record["lon"],
            "luminosity": record["luminosity"],
            "aqi":record["aqi"],
            "no":record["no"],
            "no2":record["no2"],
            "o3":record["o3"],
            "nh3":record["nh3"],
            "pm2_5":record["pm2_5"],
            "pm10":record["pm10"],
            "temperature":record["temp"],
            "humidity":record["humidity"]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051, debug=True)
