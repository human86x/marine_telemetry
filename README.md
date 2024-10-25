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
