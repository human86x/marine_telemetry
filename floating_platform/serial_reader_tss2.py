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

def read_tss_data(port, baud_rate=115200):
    """Reads turbidity (TSS) values from the serial port and returns analog, voltage, and TSS values."""
    try:
        # Open the serial port with a timeout
        ser = serial.Serial(port, baud_rate, timeout=1)  # 1-second timeout
        print(f"Connected to {port}")

        # Initialize values
        tss_value = None
        an_value = None
        volt_value = None

        while True:
            # Read a line of data from the serial port
            line = ser.readline()

            # If data is received, process it
            if line:
                try:
                    # Attempt to decode the line (assuming it's text)
                    decoded_line = line.decode().strip()

                    # Check if the line contains TSS data ("C:"), voltage ("D:"), or analog value ("E:")
                    if decoded_line.startswith("C:"):
                        an_value = decoded_line.split(":")[1].strip()  # Extract analog value
                        print(f"Analog Value: {an_value}")

                    elif decoded_line.startswith("D:"):
                        volt_value = decoded_line.split(":")[1].strip()  # Extract voltage
                        print(f"VOLTAGE: {volt_value} V")

                    elif decoded_line.startswith("E:"):
                        tss_value = decoded_line.split(":")[1].strip()  # Extract TSS value
                        print(f"TSS Value: {tss_value} NTU")

                    # Check if all values are obtained
                    if an_value is not None and volt_value is not None and tss_value is not None:
                        return an_value, volt_value, tss_value  # Return all three values

                except UnicodeDecodeError:
                    # Handle binary data or invalid encoding
                    print(f"Received (raw): {line}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        # Close the serial port if open
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Closed connection to {port}")

# Main logic
if __name__ == "__main__":
    # Read the configuration to get the correct port
    config = read_config()
    PORT = config.get('WEMOS_C_D_E_PORT')  # Adjust this key based on your config file
    BAUD_RATE = 115200  # Set your baud rate as needed

    # Call the function to start reading data
    if PORT:
        an_value, volt_value, tss_value = read_tss_data(PORT)
        print(f"Final Analog Value: {an_value}, Final Voltage Value: {volt_value}, Final TSS Value: {tss_value}")
    else:
        print("Port not found in configuration.")
