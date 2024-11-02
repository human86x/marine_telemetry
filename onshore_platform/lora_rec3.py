import serial
import time
import re
from mqtt_poster import post_to_mqtt  # Import the MQTT function

# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Adjust as necessary
baud_rate = 9600

def send_at_command(ser, command):
    """Send AT command and return the response."""
    ser.write((command + '\r\n').encode())
    time.sleep(0.5)
    response = ''
    while ser.in_waiting > 0:
        response += ser.read(ser.in_waiting).decode()
    return response.strip()

def process_message(message):
    """Process the incoming LoRa message based on its prefix."""
    try:
        sensor_type = ''
        sensor_value = None

        # Remove leading '0' if present
        if message.startswith("0"):
            message = message[1:]

        # Determine the sensor type and value
        if message.startswith("A"):  # Temperature
            sensor_type = "Temperature"
            sensor_value = float(message[1:]) / 100  # Convert to original value
            post_to_mqtt(sensor_type, sensor_value)
        elif message.startswith("B"):  # TDS
            sensor_type = "TDS"
            sensor_value = float(message[1:]) / 100
            post_to_mqtt(sensor_type, sensor_value)
        elif message.startswith("C"):  # Analog Value
            sensor_type = "Analog Value"
            sensor_value = int(message[1:])
            post_to_mqtt(sensor_type, sensor_value)
        elif message.startswith("D"):  # Voltage
            sensor_type = "Voltage"
            sensor_value = float(message[1:]) / 100
            post_to_mqtt(sensor_type, sensor_value)
        elif message.startswith("E"):  # TSS
            sensor_type = "TSS"
            sensor_value = float(message[1:]) / 100
            post_to_mqtt(sensor_type, sensor_value)
        else:
            sensor_type = "Unknown"
            sensor_value = "Invalid data"

        return sensor_type, sensor_value

    except ValueError as e:
        print(f"ValueError processing message '{message}': {e}")
        return "Unknown", "Error"
    except Exception as e:
        print(f"Error processing message: {e}")
        return "Unknown", "Error"

def main():
    last_message = None

    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to {serial_port} at {baud_rate} baud.")

        # Set to TEST mode
        mode_command = 'AT+MODE=TEST'
        response = send_at_command(ser, mode_command)

        while True:
            rx_command = 'AT+TEST=RXLRPKT'
            response = send_at_command(ser, rx_command)
            print(f"Response: **{response}**")

            # Extract hex message from the response
            pattern = r'RX "([0-9A-Fa-f]+)"'
            match = re.search(pattern, response)

            if match:
                hex_string = match.group(1)
                print(f"Extracted Hex: {hex_string}")

                try:
                    # Convert hex string back to the original message
                    raw_bytes = bytes.fromhex(hex_string)
                    converted_string = hex_string #raw_bytes.decode('utf-8', errors='replace')
                    print(f"Converted String: {converted_string}")

                    if converted_string != last_message:
                        last_message = converted_string
                        sensor_type, sensor_value = process_message(converted_string)
                        print(f"Received {sensor_type}: {sensor_value}")
                except Exception as e:
                    print(f"Error converting hex to string: {e}")
                    continue

            time.sleep(1)

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()
