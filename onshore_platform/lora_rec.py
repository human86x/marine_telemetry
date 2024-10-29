import serial
import time

# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Update if necessary
baud_rate = 9600

def send_at_command(ser, command):
    """Send AT command and return the response."""
    ser.write((command + '\r\n').encode())
    time.sleep(1)
    response = ''
    while ser.in_waiting > 0:
        response += ser.read(ser.in_waiting).decode()
    return response.strip()

def main():
    try:
        # Create a serial connection
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to {serial_port} at {baud_rate} baud.")

        # Set to TEST mode
        mode_command = 'AT+MODE=TEST'
        print(f"Sending: {mode_command}")
        response = send_at_command(ser, mode_command)
        print(f"Response: {response}")

        # Listen for incoming messages
        while True:
            # Send command to receive packet
            rx_command = 'AT+TEST=RXLRPKT'
            print(f"Sending: {rx_command}")
            response = send_at_command(ser, rx_command)
            print(f"Response: {response}")

            # Check for received message in the response
            if "RXPKT" in response:
                # Extract and print the received message
                print("Received message:", response)
            else:
                print("No new message received.")

            time.sleep(1)  # Optional delay before checking again

    except serial.SerialException as e:
        print(f"Error: {e}")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()  # Close the serial connection
            print("Serial connection closed.")

if __name__ == "__main__":
    main()

