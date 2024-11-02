import serial

# Function to read the configuration file and get the port
def read_config():
    config = {}
    try:
        with open('usb_order.config', 'r') as config_file:
            for line in config_file:
                key, value = line.strip().split('=')
                config[key] = value
    except FileNotFoundError:
        print("Configuration file not found.")
    except Exception as e:
        print(f"Error reading configuration file: {e}")
    return config

def read_sensor_data(port):
    """Reads temperature and TDS values from the serial port."""
    try:
        # Open the serial port with a timeout
        ser = serial.Serial(port, 115200, timeout=1)  # 1-second timeout
        print(f"Connected to {port}")

        temperature = None
        tds_value = None

        while True:
            # Read a line of data from the serial port
            line = ser.readline()

            # If data is received, process it
            if line:
                try:
                    # Attempt to decode the line (assuming it's text)
                    decoded_line = line.decode().strip()

                    # Check if the line contains temperature data ("A:")
                    if decoded_line.startswith("A:"):
                        temperature = decoded_line.split(":")[1].strip()  # Extract temperature value
                        print(f"Temperature: {temperature} °C")

                    # Check if the line contains TDS data ("B:")
                    elif decoded_line.startswith("B:"):
                        tds_value = decoded_line.split(":")[1].strip()  # Extract TDS value
                        print(f"TDS Value: {tds_value} ppm")

                    # If both temperature and TDS values are found, return them
                    if temperature is not None and tds_value is not None:
                        return temperature, tds_value
                    
                    # If neither, handle unexpected data
                    else:
                        print(f"Unexpected data: {decoded_line}")

                except UnicodeDecodeError:
                    # Handle binary data or invalid encoding
                    print(f"Received (raw): {line}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        # Close the serial port if open
        if ser.is_open:
            ser.close()
            print(f"Closed connection to {port}")

# Main logic
if __name__ == "__main__":
    # Read the configuration to get the correct port
    config = read_config()
    PORT = config.get('WEMOS_A_B_PORT')  # Get the port for Wemos A and B
    BAUD_RATE = 115200  # Set your baud rate as needed

    # Call the function to start reading data
    if PORT:
        read_sensor_data(PORT)
    else:
        print("Port not found in configuration.")
