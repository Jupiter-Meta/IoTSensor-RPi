import Adafruit_DHT
import paho.mqtt.client as mqtt
import json, geocoder
import time

# Define the DHT sensor type (DHT11)
DHT_SENSOR = Adafruit_DHT.DHT11

# Define the GPIO pin where the DHT sensor is connected
DHT_PIN = 4  # Replace with the actual GPIO pin number

# Define MQTT broker information
MQTT_BROKER_HOST = "65.2.135.170"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "JM/DHT"

# Initialize MQTT client
client = mqtt.Client()
location = geocoder.ip('me')
print(location)
if location.ok:
    latitude = location.latlng[0]
    longitude = location.latlng[1]
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    latitude = 0.0
    longitude = 0.0
    print("Unable to fetch location data.")

try:
    # Attempt to read data from the DHT sensor
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    # Get the current epoch timestamp
    timestamp = int(time.time())
    
    # Check if the data was successfully read
    if humidity is not None and temperature is not None:
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp,
            "lat": latitude,
            "lon": longitude
        }
        
        # Convert the data to JSON
        json_data = json.dumps(data)
        
        print("Data to be published:")
        print(json_data)
        
        # Publish the JSON data to the MQTT topic
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        client.publish(MQTT_TOPIC, json_data)
        client.disconnect()
    else:
        print("Failed to retrieve data from the DHT sensor")

except KeyboardInterrupt:
    # Exit the program if Ctrl+C is pressed
    print("Program terminated by user")
except Exception as e:
    print(f"Error: {str(e)}")
