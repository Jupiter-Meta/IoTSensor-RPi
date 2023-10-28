from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "sensor_data"

# MongoDB connection setup
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.route('/data', methods=['GET'])
def get_data():
    # Query MongoDB for data (assuming you want to retrieve all records)
    data = list(collection.find({}))
    
    # Convert MongoDB documents to a list of dictionaries
    data_list = []
    for record in data:
        data_list.append({
            "temperature": record["temperature"],
            "humidity": record["humidity"],
            "timestamp": record["timestamp"]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
