import paho.mqtt.client as mqtt

# Define your broker details
MQTT_BROKER = "localhost"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Define topics for different sensor types
MQTT_TOPICS = {
    "Temperature": "telemetry/temperature",
    "TDS": "telemetry/tds",
    "Analog Value": "telemetry/analog",
    "Voltage": "telemetry/voltage",
    "TSS": "telemetry/tss"
}

# Create the MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)

def post_to_mqtt(sensor_type, sensor_value):
    """Publish sensor data to the MQTT broker under the appropriate topic."""
    if sensor_type in MQTT_TOPICS:
        topic = MQTT_TOPICS[sensor_type]
        message = str(sensor_value)
        client.publish(topic, message)
        print(f"Published to {topic}: {message}")
    else:
        print(f"Unknown sensor type: {sensor_type}")

# If you're running this file directly, ensure the client loop is running
if __name__ == "__main__":
    client.loop_start()  # Start the loop to process network traffic
