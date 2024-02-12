import machine
import network
import socket
import urandom
import time

# Define your Wi-Fi network credentials
WIFI_SSID = "UCB Guest"
WIFI_PASSWORD = ""

# Define the IP address and port of the server
SERVER_IP = "10.200.195.152"  # Replace with the IP address of your server
SERVER_PORT = 12345           # Replace with the port number of your server

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

# Send random strings to the server
try:
    while True:
        # Generate a random string of length 10
        random_string = ''.join(chr(urandom.getrandbits(8)) for _ in range(10))
        
        # Send the random string to the server
        s.sendall(random_string.encode())
        
        # Print the sent string
        print("Sent:", random_string)
        
        # Wait for some time before sending the next string
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Close the socket
    s.close()


