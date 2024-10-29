import serial
import time
import pyudev

# Replace with the vendor ID of your LoRa module
LORA_VENDOR_ID = '10c4'  # e.g., 'xxxx'
LORA_SERIAL_NUMBER = None  # Leave as None if not using a specific serial number

# Set the ports and baud rate for Wemos devices
WEMOS_BAUD_RATE = 115200

def detect_lora_port():
    context = pyudev.Context()
    for device in context.list_devices(subsystem='tty'):
        # Check if the device matches the LoRa vendor ID
        if device.get('ID_VENDOR_ID') == LORA_VENDOR_ID:
            if LORA_SERIAL_NUMBER is None or device.get('ID_SERIAL') == LORA_SERIAL_NUMBER:
                return device.device_node  # Return the device node (e.g., /dev/ttyUSB0)
    return None

def try_connect(port, baud_rate, command):
    try:
        with serial.Serial(port, baud_rate, timeout=2) as ser:
            time.sleep(2)  # Wait for the connection to establish
            ser.write(command.encode())
            time.sleep(1)  # Wait for the response
            response = ser.read_all().decode(errors='ignore').strip()
            return response
    except serial.SerialException as e:
        print(f"Could not open {port}: {e}")
        return None

def write_config(wemos_a_b_port, wemos_c_d_e_port, lora_port):
    with open('usb_order.config', 'w') as config_file:
        config_file.write(f"WEMOS_A_B_PORT={wemos_a_b_port}\n")
        config_file.write(f"WEMOS_C_D_E_PORT={wemos_c_d_e_port}\n")
        config_file.write(f"LORA_PORT={lora_port}\n")
    print(f"\nDevice configuration written to usb_order.config")

def main():
    lora_port = detect_lora_port()
    wemos_a_b_port = None
    wemos_c_d_e_port = None

    available_ports = [port for port in pyudev.Context().list_devices(subsystem='tty') if port.device_node.startswith('/dev/ttyUSB')]

    for port in available_ports:
        # Try connecting to the first Wemos device
        print(f"Trying to connect to {port.device_node} for Wemos device A...")
        response = try_connect(port.device_node, WEMOS_BAUD_RATE, "")
        
        if response is not None and "A:" in response and "B:" in response:
            wemos_a_b_port = port.device_node
            print(f"Connected to Wemos device A on {port.device_node}")
            print(f"Output: {response}")
            continue  # Move to the next port

        # Try connecting to the second Wemos device
        print(f"Trying to connect to {port.device_node} for Wemos device B...")
        response = try_connect(port.device_node, WEMOS_BAUD_RATE, "")
        
        if response is not None and "C:" in response and "D:" in response and "E:" in response:
            wemos_c_d_e_port = port.device_node
            print(f"Connected to Wemos device B on {port.device_node}")
            print(f"Output: {response}")
            continue

    # Final output of connections
    print("\nSummary of Connections:")
    if wemos_a_b_port:
        print(f"First Wemos (A and B): {wemos_a_b_port}")
    else:
        print("First Wemos (A and B): Not found")

    if wemos_c_d_e_port:
        print(f"Second Wemos (C, D, and E): {wemos_c_d_e_port}")
    else:
        print("Second Wemos (C, D, and E): Not found")

    if lora_port:
        print(f"LoRa Module: {lora_port}")
    else:
        print("LoRa Module: Not found")

    # Write the configuration to a file
    write_config(wemos_a_b_port, wemos_c_d_e_port, lora_port)

if __name__ == "__main__":
    main()
