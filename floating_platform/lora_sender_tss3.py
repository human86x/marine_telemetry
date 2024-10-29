import serial
import time
from serial_reader_tds import read_sensor_data  # Import the external sensor reader
from serial_reader_tss2 import read_tss_data  # Import TSS reader

# Function to read configuration from the file
def read_config(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):  # Skip empty lines and comments
                key, value = line.strip().split('=')
                config[key] = value
    return config

# Read the port configurations from the config file
config = read_config('usb_order.config')
SERIAL_PORT = config['LORA_PORT']  # Read LoRa port from config
BAUD_RATE = 9600

# Set up the serial connection for LoRa
def setup_connection():
    """Establish a serial connection to the LoRa module."""
    try:
        e5 = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=2)
        time.sleep(2)  # Allow some time for the connection to establish
        print(f"Connected to LoRa module on {SERIAL_PORT}")
        return e5
    except Exception as e:
        print(f"Error opening serial port: {e}")
        exit(1)

def send_command(e5, command):
    """Send an AT command to the Wio E5 module and read the response."""
    e5.write(f"{command}\r\n".encode('utf-8'))  # Send command
    time.sleep(0.5)  # Delay for the module to respond
    response = e5.read_all()  # Read response as bytes
    try:
        decoded_response = response.decode('utf-8')  # Attempt to decode as UTF-8
        print(f"Command Sent: {command.strip()}\nResponse: {decoded_response.strip()}")  # Print response
    except UnicodeDecodeError:
        print(f"Command Sent: {command.strip()}\nResponse: (Decoding Error) Raw bytes: {response}")  # Print raw bytes
        decoded_response = ""  # Set decoded response to empty string on error
    return decoded_response

def format_data(label, value):
    """Format the data by removing decimal points and handling negative signs."""
    value = float(value)  # Ensure the value is a float
    if value < 0:
        value = abs(value)  # Convert negative value to positive
    return f"{label}{int(value * 100)}"  # Convert float to integer by multiplying by 100

# Set up the LoRa module connection
e5 = setup_connection()

# Set up the LoRa module
send_command(e5, "AT")  # Test AT command
send_command(e5, "AT+MODE=TEST")  # Set to TEST mode

# Keep sending the temperature, TDS, and TSS via LoRa indefinitely
try:
    while True:
        # Read the temperature and TDS values from the first serial reader
        temperature, tds_value = read_sensor_data(config['WEMOS_A_B_PORT'])  # Use port from config
        
        # Read the TSS data (analog value, voltage, TSS value)
        an_value, volt_value, tss_value = read_tss_data(config['WEMOS_C_D_E_PORT'])  # Use port from config

        # Check if all readings are valid before sending
        if temperature and tds_value and an_value and volt_value and tss_value:
            # Convert values to float if necessary
            temperature = float(temperature)
            tds_value = float(tds_value)
            an_value = int(an_value)
            volt_value = float(volt_value)
            tss_value = float(tss_value)

            # Format messages to send
            temp_message = format_data("A", temperature)  # Temperature
            tds_message = format_data("B", tds_value)     # TDS
            tss_message = format_data("E", tss_value)     # TSS
            an_message = format_data("C", an_value)       # Analog Value
            volt_message = format_data("D", volt_value)   # Voltage

            # Print messages for debugging
            print(f"Sending Temperature: {temp_message}")
            print(f"Sending TDS Value: {tds_message}")
            print(f"Sending TSS Value: {tss_message}")
            print(f"Sending Analog Value: {an_message}")
            print(f"Sending Voltage: {volt_message}")

            # Send the messages via LoRa and check responses
            for message in [temp_message, tds_message, tss_message, an_message, volt_message]:
                response = send_command(e5, f'AT+TEST=TXLRPKT, "{message}"')
                # Check if the response is empty
                if not response.strip():
                    print("Empty response received, reconnecting...")
                    e5.close()  # Close the current connection
                    e5 = setup_connection()  # Re-establish the connection
                    break  # Exit the for loop to start sending again

        time.sleep(5)  # Wait for a bit before the next reading

except KeyboardInterrupt:
    print("Program terminated")

# Clean up
if e5.is_open:
    e5.close()  # Close the serial connection
