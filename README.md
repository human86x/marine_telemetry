Marine Telemetry IoT System
Project Overview
This marine telemetry IoT system is a proof of concept for monitoring environmental data remotely from a floating platform, an onshore platform, and an observational center. The floating platform captures real-time data on temperature, Total Dissolved Solids (TDS), and Total Suspended Solids (TSS) using various sensors, transmitting it via LoRa to the onshore platform for data processing, storage, and future analysis.

Floating Platform: Raspberry Pi Zero 2 W, Wio E5 Mini LoRa, two Wemos D1 Minis with Dallas temperature, TDS, and TSS sensors, powered by a solar power bank.
Onshore Platform: Raspberry Pi Zero 2 W and Wio E5 Mini LoRa, listening to incoming LoRa messages, posting data to an MQTT broker.
Observational Center: Accesses data via Wi-Fi for remote viewing and analysis.
Status: Devices are currently housed in makeshift enclosures for functional testing, with sensors tested in water cups. Deployment on water is pending further testing.

System Architecture

Floating Platform captures and sends sensor data via LoRa.
Onshore Platform receives LoRa transmissions, sends data to an MQTT broker.
Observational Center connects to the onshore platform via Wi-Fi to view data.
Components
Floating Platform
Hardware:
Raspberry Pi Zero 2 W
Wio E5 Mini LoRa Module
2 x Wemos D1 Minis
Wemos 1: Dallas temperature sensor + DFRobot SEN0244 TDS sensor
Wemos 2: DFRobot SEN0189 TSS sensor
Solar power bank
Software:
Arduino sketches for Wemos devices to read sensors and transmit data via USB serial to the Pi.
Python script on Raspberry Pi to read data from Wemos and re-send via LoRa.
Onshore Platform
Hardware:
Raspberry Pi Zero 2 W
Wio E5 Mini LoRa Module
Software:
Python script to listen for LoRa messages, parse sensor data, and publish it to an MQTT broker on localhost.
Observational Center
Hardware: Computer or mobile device
Software: MQTT client to view transmitted data via Wi-Fi.
Setup Guide
1. Prerequisites
Hardware setup:
Connect sensors to respective Wemos devices and ensure the LoRa modules are wired correctly to the Raspberry Pi's USB ports.
Power the floating platform with a solar power bank.
Software requirements:
Arduino IDE for Wemos programming.
Python 3.12.3 (or compatible version) on the Raspberry Pi devices.
MQTT broker setup on the Onshore Platform Pi (e.g., Mosquitto).
2. Installation
Clone Repository:

bash
Copy code
git clone https://github.com/yourusername/marine-telemetry-iot-system.git
cd marine-telemetry-iot-system
Configure Wemos Devices:

Flash Wemos devices with provided Arduino sketches in /Floating_Platform/Wemos_Scripts.
Install Python Dependencies:

On Raspberry Pi devices, navigate to the project directory and install required packages:
bash
Copy code
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements.txt
Ensure MQTT broker (e.g., Mosquitto) is running on the Onshore Platform.
Configuration Files:

Edit usb_order.config to map USB devices consistently for serial communication.
Modify MQTT settings in Python scripts if needed.
3. Running the System
Start Floating Platform:

Power up the floating platform.
Run the Python script to begin reading data from Wemos and transmitting via LoRa:
bash
Copy code
python3 Floating_Platform/main.py
Start Onshore Platform:

Run the LoRa listening script on the Onshore Platform to begin receiving data:
bash
Copy code
python3 Onshore_Platform/main.py
Access Data:

Connect to the MQTT broker from a computer or mobile device on the same network as the Onshore Platform to view live data.
Future Plans
Hardware Upgrades: Replace temporary housings with durable, waterproof enclosures.
Data Analysis: Implement data storage and analysis, with potential future integration of AI for predictive modeling.
Expanded Deployment: Deploy the floating platform on water for full-scale testing.
Contributions
Contributions to improve system functionality, data analysis, and housing durability are welcome! Please feel free to fork this repository and submit a pull request.

