# **Sea4Us Marine Telemetry IoT System: Quick Start Guide**

This document provides step-by-step instructions for powering up and using the marine telemetry IoT system prototype. The system includes a **floating platform** and an **onshore platform** to monitor environmental measurements such as temperature, Total Dissolved Solids (TDS), and Total Suspended Solids (TSS). Data is transmitted via LoRa and accessed through the onshore platform's MQTT broker.

---

## **System Components**
1. **Floating Platform**
   - Raspberry Pi Zero 2 W
   - Wio E5 Mini LoRa module
   - Two Wemos D1 Minis with temperature, TDS, and TSS sensors
   - Solar Power Bank

2. **Onshore Platform**
   - Raspberry Pi Zero 2 W
   - Wio E5 Mini LoRa module
   - MQTT Broker

---

## **Quick Start Instructions**

### **1. Power On the Floating Platform**
1. Connect the solar power bank to the floating platform's Raspberry Pi.
2. Wait ~2 minutes for the system to boot.
3. Observe the **blue LED on the LoRa device**:
   - **Blinking** indicates that data transmission has started successfully.

### **2. Power On the Onshore Platform**
1. Connect the solar power bank to the onshore platform's Raspberry Pi.
2. Wait ~2 minutes for the system to boot.
3. Observe the **blue LED on the LoRa device**:
   - **Blinking** indicates the system is ready to receive data.

### **3. Access Measurement Data**
- Open a browser or MQTT client on a device connected to the same network.
- Access the MQTT broker using the **local IP address** of the onshore platform's Raspberry Pi:
  ```
  mqtt://<local-ip>:1883
  ```
  Example:
  ```
  mqtt://192.168.1.144:1883
  ```
- Alternatively, access the broker via the **external IP address** if the router's port forwarding is enabled. The router has already been configured to forward external requests to **port 1883**, allowing measurements to be accessed from anywhere using an MQTT subscriber app.

### **4. Verify Data Transmission**
- Use an MQTT client like **MQTT Explorer** to subscribe to topics and view real-time data:
  - Temperature: `floating/temperature`
  - TDS: `floating/tds`
  - TSS: `floating/tss`
- Data will continuously update once both platforms are active.

---

## **Remote Access**
Since the router is already configured to forward external IP requests to **port 1883** on the onshore platform, you can access measurements using an MQTT subscriber app from anywhere. Use the following details:
- **Broker Address:** `<external-ip>:1883`
- **Example Topics:**
  - `floating/temperature`
  - `floating/tds`
  - `floating/tss`

---

## **Troubleshooting**
1. **No Blinking LED on LoRa Module:**
   - Ensure the power bank is connected and fully charged.
   - Verify USB connections to the Raspberry Pi and LoRa module.

2. **No Data on MQTT Broker:**
   - Confirm both platforms are powered and operational.
   - Check the Raspberry Pi's IP addresses using a network scanner (e.g., `nmap`).
   - Ensure the router's port forwarding is properly configured.

---

## **Notes**
- The floating platform must be powered on **before** the onshore platform.
- Data can be accessed via local or external IP, depending on network configuration.
- If unsure about IP addresses or port forwarding, contact the network administrator.
