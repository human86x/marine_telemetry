# Marine Telemetry IoT System

## Project Overview

This marine telemetry IoT system is a proof of concept for monitoring environmental data remotely using a **floating platform**, **onshore platform**, and an **observational center**. The floating platform captures real-time data on temperature, Total Dissolved Solids (TDS), and Total Suspended Solids (TSS) using various sensors, then transmits it via LoRa to the onshore platform for data processing, storage, and future analysis.

[![Watch the video](https://img.youtube.com/vi/xaF3v0I2ETI/maxresdefault.jpg)](https://www.youtube.com/watch?v=xaF3v0I2ETI)


### Platforms and Data Flow

- **Floating Platform**: 
   - *Hardware*: Raspberry Pi Zero 2 W, Wio E5 Mini LoRa, two Wemos D1 Minis with Dallas temperature, TDS, and TSS sensors, all powered by a solar power bank.
   - *Function*: Collects sensor data and sends it via LoRa to the onshore platform.

- **Onshore Platform**:
   - *Hardware*: Raspberry Pi Zero 2 W and Wio E5 Mini LoRa.
   - *Function*: Receives incoming LoRa messages, then posts data to an MQTT broker.

- **Observational Center**:
   - *Access*: Data is accessed via Wi-Fi for remote monitoring and analysis.

- **Current Status**: 
   - Devices are housed in makeshift enclosures for functional testing, with sensors tested in water containers. Deployment on water is pending further testing.

---

## System Architecture

1. **Floating Platform**: Captures and transmits sensor data via LoRa.
2. **Onshore Platform**: Receives LoRa transmissions and posts data to an MQTT broker.
3. **Observational Center**: Connects to the onshore platform via Wi-Fi to access data.

---

## Components

### Floating Platform

**Hardware**:
- **Raspberry Pi Zero 2 W**
- **Wio E5 Mini LoRa Module**
- **2 x Wemos D1 Minis**
   - **Wemos 1**: Dallas temperature sensor + DFRobot SEN0244 TDS sensor
   - **Wemos 2**: DFRobot SEN0189 TSS sensor
- **Solar Power Bank**

**Software**:
- **Arduino Sketches**: Code for Wemos devices to read sensors and transmit data via USB serial to the Raspberry Pi.
- **Python Script**: Runs on the Raspberry Pi to read data from Wemos and re-transmit via LoRa.

### Onshore Platform

**Hardware**:
- **Raspberry Pi Zero 2 W**
- **Wio E5 Mini LoRa Module**

**Software**:
- **Python Script**: Listens for LoRa messages, parses sensor data, and publishes it to an MQTT broker on localhost.

### Observational Center

**Hardware**:
- Computer or mobile device

**Software**:
- **MQTT Client**: For viewing transmitted data via Wi-Fi.

---

## Setup Guide

### Prerequisites

Ensure the following hardware is set up and ready:
1. Raspberry Pi Zero 2 W with configured OS.
2. Wemos D1 Minis with appropriate sensors connected.
3. Wio E5 Mini LoRa modules.
4. MQTT broker configured on the onshore platform.

---

## Setup Guide

### Prerequisites

1. **Install Raspberry Pi OS** on a microSD card. 
   - Ensure Wi-Fi credentials are configured so you can access the Pi on the same network.
   - Activate SSH for remote access.

### Hardware Setup

1. **Power the Raspberry Pi** using a solar power bank. 
2. Wait a couple of minutes, then use another device to get a list of connected devices on the network to identify the Raspberry Pi's IP address:
   ```bash
   nmap -sP xxx.xxx.xxx.0/24
   ```
3. **Connect to the Raspberry Pi** using SSH:
   ```bash
   ssh -p 22 username@xxx.xxx.xxx.xxx
   ```

### File Transfer

1. After a successful connection, copy the floating platform Python files to the user directory:
   ```bash
   scp username@<IP Address of Raspberry Pi>:<Path to File> .
   ```

### Configure Services on Raspberry Pi

1. **Create a service file for `usb_order.py`:**
   - Navigate to `/etc/systemd/system/` and create a file named `usb_order.service`.

   ```ini
   [Unit]
   Description=Run usb_order.py at boot with a delay
   After=network.target

   [Service]
   ExecStart=/bin/bash -c 'sleep 30; /usr/bin/python /home/sensor/usb_order.py'
   WorkingDirectory=/home/sensor/
   StandardOutput=journal
   StandardError=journal
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   - Change the Python directory and home directory according to your setup.

2. **Create a service file for `watcher.py`:**
   - In the same folder, create another file named `watcher.service`.

   ```ini
   [Unit]
   Description=Run watcher.py at boot with a delay
   After=network.target

   [Service]
   ExecStart=/bin/bash -c 'sleep 60; /usr/bin/python /home/sensor/watcher.py'
   WorkingDirectory=/home/sensor/
   StandardOutput=journal
   StandardError=journal
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable the services:**
   ```bash
   sudo systemctl enable usb_order.service
   sudo systemctl enable watcher.service
   sudo systemctl daemon-reload
   ```

### Python Environment Setup

1. **Prepare the Python environment** for the scripts.
   - Install the necessary library on the floating platform: `pyserial`, which is essential for communicating with the LoRa and Wemos devices.
   - Install it using your preferred method (pip or apt):
   ```bash
   pip install pyserial
   ```
   or 
   ```bash
   sudo apt install python3-pyserial
   ```

### Wemos Device Configuration

#### Prerequisite: Arduino IDE Installation and Configuration

1. **Install the Arduino IDE** on your computer.
2. **Add ESP8266 Board Support**:
   - Go to **File > Preferences**.
   - In the "Additional Board Manager URLs" field, add the following URL:
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Go to **Tools > Board > Board Manager**, search for "ESP8266," and install the ESP8266 board package.
3. **Install Required Libraries**:
   - Go to **Sketch > Include Library > Manage Libraries** and search for the following libraries:
     - **DallasTemperature** (for the DS18B20 temperature sensor).
     - **OneWire** (required for DallasTemperature).
   - Install these libraries to enable sensor functionality on the Wemos devices.

---

#### Wemos 1 Setup

##### Hardware Setup

1. **Connect the TDS Sensor** to Wemos 1:
   - GND (Ground)
   - VCC (3.3V)
   - A0 (Analog Pin)

2. **Connect the Dallas Temperature Sensor** (DS18B20) to Wemos 1:
   - GND (Ground)
   - VCC (5V)
   - D4 (Data Pin)
   - Connect a **4.7k ohm resistor** between VCC and the data pin of the DS18B20 sensor.

##### Software Setup

1. **Open the Wemos 1 Arduino Sketch**:
   - Locate and open the `wemos_1` sketch in the Arduino IDE.
2. **Select the Board and Port**:
   - Set the board to **LOLIN(WEMOS) D1 R2 & mini** under **Tools > Board**.
   - Select the correct **Port**.
3. **Compile and Upload**:
   - Compile the sketch and upload it to Wemos 1.
4. **Verify Data Transmission**:
   - Open the **Serial Monitor** (set to **115200 baud**) to check data. You should see output similar to:
     ```
     A: xx.xx  (temperature in °C)
     B: xxx.xx (TDS value in ppm)
     ```

---

#### Wemos 2 Setup

##### Hardware Setup

1. **Connect the TSS Sensor** to Wemos 2:
   - GND (Ground)
   - VCC (3.3V)
   - A0 (Analog Pin)

##### Software Setup

1. **Open the Wemos 2 Arduino Sketch**:
   - Locate and open the `wemos_2` sketch in the Arduino IDE.
2. **Select the Board and Port**:
   - Set the board to **LOLIN(WEMOS) D1 R2 & mini** under **Tools > Board**.
   - Select the correct **Port**.
3. **Compile and Upload**:
   - Compile the sketch and upload it to Wemos 2.
4. **Verify Data Transmission**:
   - Open the **Serial Monitor** (set to **115200 baud**) to check data. You should see output similar to:
     ```
     C: XX    (analog value)
     D: XX.XX (voltage)
     E: XXXX  (TSS value in mg/L)
     ```

---


### Final Connections

1. Connect both Wemos devices and the LoRa module to a USB hub and connect it to the Raspberry Pi.
2. **Reboot the Raspberry Pi.** The script will identify the devices by their output and create a config file mapping `ttyUSB` ports, which is crucial for communication due to device ID similarities.

### Monitoring Setup

1. When the watcher service starts, it will send an email to the preconfigured address containing the internal and external IP addresses of the Raspberry Pi, along with a log file from the watcher service.
   - If you are using Gmail, generate an access token for the application and insert it into the code.
