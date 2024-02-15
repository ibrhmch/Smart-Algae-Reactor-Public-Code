import machine
import onewire
import ds18x20
import time

# Define the GPIO pin connected to the DS18B20 data line
pin = machine.Pin(0)  # Use the GPIO pin where you connected the DS18B20 data line

# Create a OneWire instance
ow = onewire.OneWire(pin)

# Create a DS18X20 instance
ds = ds18x20.DS18X20(ow)

# Scan for DS18B20 devices on the OneWire bus
roms = ds.scan()

if not roms:
    print("No DS18B20 devices found. Check your connections.")
    # sys.exit()

try:
    while True:
        # Trigger temperature conversion
        ds.convert_temp()

        # Wait for the conversion to complete (750ms for DS18B20)
        time.sleep_ms(750)

        # Read temperature from all DS18B20 devices
        for rom in roms:
            temperature = ds.read_temp(rom)
            print(f"Temperature (Device {rom.hex()}): {temperature:.2f} °C")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
