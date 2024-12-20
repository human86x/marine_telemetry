import serial
import time
import os

# Replace with the vendor ID of your LoRa module
LORA_VENDOR_ID = '10c4'  # e.g., 'xxxx'
LORA_SERIAL_NUMBER = None  # Leave as None if not using a specific serial number

# Set the ports and baud rate for Wemos devices
WEMOS_BAUD_RATE = 115200

def detect_lora_port():
    # Check the /dev directory for USB devices
    for device in os.listdir('/dev'):
        if device.startswith('ttyUSB'):
            # You can add checks here to match the vendor ID or serial number if needed
            # This is a placeholder; actual implementation would require parsing vendor info
            return f"/dev/{device}"  # Return the device node (e.g., /dev/ttyUSB0)
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

    # Check for available ttyUSB devices
    available_ports = [f"/dev/{port}" for port in os.listdir('/dev') if port.startswith('ttyUSB')]

    for port in available_ports:
        # Try connecting to the first Wemos device
        print(f"Trying to connect to {port} for Wemos device A...")
        response = try_connect(port, WEMOS_BAUD_RATE, "")
        
        if response is not None and "A:" in response and "B:" in response:
            wemos_a_b_port = port
            print(f"Connected to Wemos device A on {port}")
            print(f"Output: {response}")
            continue  # Move to the next port

        # Try connecting to the second Wemos device
        print(f"Trying to connect to {port} for Wemos device B...")
        response = try_connect(port, WEMOS_BAUD_RATE, "")
        
        if response is not None and "C:" in response and "D:" in response and "E:" in response:
            wemos_c_d_e_port = port
            print(f"Connected to Wemos device B on {port}")
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
