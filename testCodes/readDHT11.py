import Adafruit_DHT

# Define the DHT sensor type (DHT11)
DHT_SENSOR = Adafruit_DHT.DHT11

# Define the GPIO pin where the DHT sensor is connected
DHT_PIN = 4  # Replace with the actual GPIO pin number

try:
    # Attempt to read data from the DHT sensor
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    # Check if the data was successfully read
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.2f}°C")
        print(f"Humidity: {humidity:.2f}%")
    else:
        print("Failed to retrieve data from the DHT sensor")

except KeyboardInterrupt:
    # Exit the program if Ctrl+C is pressed
    print("Program terminated by user")
except Exception as e:
    print(f"Error: {str(e)}")
