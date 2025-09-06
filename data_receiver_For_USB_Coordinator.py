#!/usr/bin/python

"""
****************************************************************************************************
Date       : 6-April-2025
Title : Real-Time SenML Sensor Data Receiver via XBee on Raspberry Pi
Summary:
This Python script is executed on a Raspberry Pi (or PC) to receive sensor data wirelessly from 
an Arduino-based end node via XBee (DigiMesh S2C). The data is sent in JSON (SenML) format from 
a DHT11 sensor (temperature/humidity), read by Arduino, and transmitted using XBee.

The Raspberry Pi acts as a gateway (coordinator) and listens on a specified serial port for 
incoming data using the XBee module connected via USB.

Key Steps:
1. Configure XBee modules using XCTU as coordinator and end node.
2. Connect the XBee module to Raspberry Pi via USB and run this script.
3. When data is received, decode the RF payload, check its length, and parse it as JSON.
4. Extract and print the values from the SenML format object.
5. Handles JSON errors and gracefully exits on user interrupt.

SenML Format Sample:
{"bn":"Arduino uno Node1","n":"temperature","u":"Cel","v":24.5}

****************************************************************************************************
"""

from xbee import ZigBee
from datetime import datetime
import serial
# import requests  # Uncomment if you're posting data to a web server
import struct
# import sensor_data_to_xml  # Optional for XML conversion

import os
import sys
import psutil
import logging
import json

# Serial port and baud rate for XBee USB connection
PORT = 'COM3'  # Use '/dev/ttyUSB0' for Linux or 'COMx' for Windows
BAUD_RATE = 9600

# Initialize serial connection and XBee interface
ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser, escaped=True)

print("Listening for XBee data on", PORT, "at", BAUD_RATE, "baud...\n")

# Main loop to continuously listen for XBee frames
while True:
    try:
        print("Waiting for XBee data...")
        response = xbee.wait_read_frame()

        # Extract source addresses from the frame
        sourceAddressLong = ''.join('%02x' % b for b in response['source_addr_long'])
        sourceAddressShort = ''.join('%02x' % b for b in response['source_addr_long'][4:])

        # Decode RF (radio frequency) data as string
        rf = response['rf_data'].decode('utf-8', errors='ignore')
        datalength = len(rf)

        print("Raw RF data:", rf)
        print("Data length:", datalength)

        # Check if data length matches expected SenML payload
        if datalength == 66:
            try:
                # Parse SenML JSON string
                jsonData = json.loads(rf)
                baseName = jsonData["bn"]
                name = jsonData["n"]
                unit = jsonData["u"]
                value = jsonData["v"]

                # Display the extracted values
                print("Source Address:", sourceAddressLong)
                print("Base Name:", baseName)
                print("Name:", name)
                print("Unit:", unit)
                print("Value:", value)
                print("\n")
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
        else:
            print("Data format doesn't match expected length. Skipping...\n")

    except KeyboardInterrupt:
        print("Exiting...")
        break

# Close serial connection gracefully
ser.close()
