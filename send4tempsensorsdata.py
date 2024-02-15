import json
import socket
import time

import ds18x20
import machine
import network
import onewire

"""
This script starts a client that reads temperature data from four DS18B20 sensors.
The temperature data is sent to a server as a JSON string over a TCP socket.
"""

# Define your Wi-Fi network credentials
WIFI_SSID = "UCB Guest"
WIFI_PASSWORD = ""

# Define the IP address and port of the server
SERVER_IP = "10.200.195.244"  # Replace with the IP address of your server
SERVER_PORT = 12345  # Replace with the port number of your server

# Connect to Wi-Fi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait until connected to Wi-Fi
while not sta_if.isconnected():
    time.sleep(1)

print("Connected to Wi-Fi")

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
s.connect((SERVER_IP, SERVER_PORT))

# Define the GPIO pins connected to the DS18B20 data lines
pin = machine.Pin(0)  # Use the GPIO pin where you connected the first DS18B20 data line
pin1 = machine.Pin(
    4
)  # Use the GPIO pin where you connected the second DS18B20 data line
pin2 = machine.Pin(
    8
)  # Use the GPIO pin where you connected the third DS18B20 data line
pin3 = machine.Pin(
    12
)  # Use the GPIO pin where you connected the third DS18B20 data line

# Create OneWire instances for each pin
ow = onewire.OneWire(pin)
ow1 = onewire.OneWire(pin1)
ow2 = onewire.OneWire(pin2)
ow3 = onewire.OneWire(pin3)

# Create DS18X20 instances for each OneWire instance
ds = ds18x20.DS18X20(ow)
ds1 = ds18x20.DS18X20(ow1)
ds2 = ds18x20.DS18X20(ow2)
ds3 = ds18x20.DS18X20(ow3)

# Scan for DS18B20 devices on each OneWire bus
roms = ds.scan()
roms1 = ds1.scan()
roms2 = ds2.scan()
roms3 = ds3.scan()

if not roms or not roms1 or not roms2 or not roms3:
    print("No DS18B20 devices found. Check your connections.")
    # sys.exit()

try:
    while True:
        # Trigger temperature conversion for each DS18X20 instance
        ds.convert_temp()
        ds1.convert_temp()
        ds2.convert_temp()
        ds3.convert_temp()

        # Wait for the conversion to complete (750ms for DS18B20)
        time.sleep_ms(750)

        # Read temperature from all DS18B20 devices on each OneWire bus
        temperature_data = {}

        for i, rom in enumerate(roms):
            temperature = ds.read_temp(rom)
            temperature_data[f"TD{i + 1}"] = round(temperature, 2)

        for i, rom in enumerate(roms1):
            temperature = ds1.read_temp(rom)
            temperature_data[f"TD{i + 1 + len(roms)}"] = round(temperature, 2)

        for i, rom in enumerate(roms2):
            temperature = ds2.read_temp(rom)
            temperature_data[f"TD{i + 1 + len(roms) + len(roms1)}"] = round(
                temperature, 2
            )

        for i, rom in enumerate(roms3):
            temperature = ds3.read_temp(rom)
            temperature_data[f"TD{i + 1 + len(roms) + len(roms1) + len(roms2)}"] = (
                round(temperature, 2)
            )

        # Send temperature data as JSON
        s.sendall(json.dumps(temperature_data).encode())

        time.sleep(5)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Close the socket
    s.close()
