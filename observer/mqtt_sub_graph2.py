import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from collections import deque
import re
import time

# Define MQTT settings
MQTT_BROKER = "192.168.12.129"  # Replace with your broker IP address
MQTT_PORT = 1883
MQTT_TOPIC = "telemetry"  # Replace with your topic

# Initialize deques to store sensor data separately
temp_data_queue = deque(maxlen=100)
tds_data_queue = deque(maxlen=100)
analog_data_queue = deque(maxlen=100)
voltage_data_queue = deque(maxlen=100)
tss_data_queue = deque(maxlen=100)

# Create a figure for real-time plotting
plt.ion()  # Interactive mode on
fig, axes = plt.subplots(5, 1)  # Five subplots for each sensor type

def on_message(client, userdata, message):
    """Callback for when a PUBLISH message is received."""
    message_str = message.payload.decode('utf-8')

    # Use regex to extract sensor type and value
    match = re.match(r'(\w+):\s*([\d.]+)', message_str)  # Matches sensor_type: value format
    if match:
        sensor_type = match.group(1)
        sensor_value = float(match.group(2))

        if sensor_type == 'Temperature':
            print(f"Temperature value: {sensor_value}")
            temp_data_queue.append(sensor_value)
        elif sensor_type == 'TDS':
            print(f"TDS value: {sensor_value}")
            tds_data_queue.append(sensor_value)
        elif sensor_type == 'Analog Value':
            print(f"REQUESTING: {sensor_type}")
            print(f"Analog Value: {sensor_value}")
            analog_data_queue.append(sensor_value)
        elif sensor_type == 'Voltage':
            print(f"Voltage: {sensor_value}")
            voltage_data_queue.append(sensor_value)
        elif sensor_type == 'TSS':
            print(f"TSS value: {sensor_value}")
            tss_data_queue.append(sensor_value)

        # Update the graph
        update_plot()
    else:
        print(f"Received message doesn't match expected format: {message_str}")
        #print(f"REQUESTING: {sensor_type}")

def update_plot():
    """Update the matplotlib plot with new data."""
    # Clear the previous plots
    for ax in axes:
        ax.clear()

    # Set labels and plot the data for each sensor
    axes[0].set_title("Temperature Over Time")
    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("Temperature (°C)")
    if temp_data_queue:
        axes[0].plot(list(range(len(temp_data_queue))), list(temp_data_queue), 'r-', label="Temperature")

    axes[1].set_title("TDS Over Time")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("TDS (ppm)")
    if tds_data_queue:
        axes[1].plot(list(range(len(tds_data_queue))), list(tds_data_queue), 'b-', label="TDS")

    axes[2].set_title("Analog Value Over Time")
    axes[2].set_xlabel("Time")
    axes[2].set_ylabel("Analog Value")
    if analog_data_queue:
        axes[2].plot(list(range(len(analog_data_queue))), list(analog_data_queue), 'g-', label="Analog Value")

    axes[3].set_title("Voltage Over Time")
    axes[3].set_xlabel("Time")
    axes[3].set_ylabel("Voltage (V)")
    if voltage_data_queue:
        axes[3].plot(list(range(len(voltage_data_queue))), list(voltage_data_queue), 'm-', label="Voltage")

    axes[4].set_title("TSS Over Time")
    axes[4].set_xlabel("Time")
    axes[4].set_ylabel("TSS")
    if tss_data_queue:
        axes[4].plot(list(range(len(tss_data_queue))), list(tss_data_queue), 'c-', label="TSS")

    # Draw the updated plots
    plt.draw()
    plt.pause(0.01)

def main():
    # Create an MQTT client instance
    client = mqtt.Client()

    # Set the callback for received messages
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Subscribe to the topic
    client.subscribe(MQTT_TOPIC)

    # Run the MQTT loop in the main thread instead of a background thread
    try:
        # Keep the plot and MQTT client running together
        while True:
            client.loop(timeout=0.01)  # Process incoming messages
            plt.pause(0.1)  # Keep the plot open and responsive
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Clean up when exiting
        client.disconnect()

if __name__ == "__main__":
    main()
