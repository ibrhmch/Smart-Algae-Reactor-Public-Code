import csv
import datetime
import json
import socket

import matplotlib.pyplot as plt

HOST = "10.200.195.244"  # Listen on this interface
PORT = 12345  # Arbitrary port number


# Function to save data to CSV file
def save_to_csv(data):
    with open("temperature_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)


# Function to plot temperature data
def plot_temperature(data):
    # Plot the temperature data
    try:
        plt.figure(figsize=(8, 6))  # Set figure size

        # Plot each sensor's temperature readings
        for i, (sensor, temperatures) in enumerate(data.items(), start=1):
            plt.plot(
                range(1, len(temperatures) + 1), temperatures, marker="o", label=sensor
            )

        plt.xlabel("Measurement Index")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature Measurements")
        plt.legend()  # Show legend with sensor names
        plt.grid(True)
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.savefig("temperature_plot.png")
        plt.show(block=False)  # Show plot without blocking script execution

        # Pause for a short duration to allow the plot to refresh
        plt.pause(0.1)

        # Close the plot to release resources and avoid multiple plots
        plt.close()
    except Exception as e:
        print("Error plotting temperature:", e)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    tempdata = {
        "TD1": [],
        "TD2": [],
        "TD3": [],
        "TD4": [],
    }
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break

            # Decode the JSON data
            json_data = json.loads(data.decode())

            # Process the received temperature data
            print("Received:", json_data)
            for key, value in json_data.items():
                tempdata[key].append(float(value))

            # Save data to CSV file
            # Note: Uncomment the following line if you want to save data to CSV
            save_to_csv(
                [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                + list(json_data.values())
            )

            # Plot temperature data
            # Note: Uncomment the following line if you want to plot the data
            # plot_temperature(tempdata)
