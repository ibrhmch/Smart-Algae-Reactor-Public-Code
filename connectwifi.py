import socket
from time import sleep

import machine
import network
from picozero import pico_led, pico_temp_sensor

ssid = "UCB Guest"
password = ""


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
