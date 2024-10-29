# Marine Telemetry IoT System

## Project Overview

This marine telemetry IoT system is a proof of concept for monitoring environmental data remotely using a **floating platform**, **onshore platform**, and an **observational center**. The floating platform captures real-time data on temperature, Total Dissolved Solids (TDS), and Total Suspended Solids (TSS) using various sensors, then transmits it via LoRa to the onshore platform for data processing, storage, and future analysis.

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

