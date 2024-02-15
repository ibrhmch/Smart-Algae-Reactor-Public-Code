import machine
import onewire
import ds18x20
import time

# Define the GPIO pins connected to the DS18B20 data lines
pin = machine.Pin(0)   # Use the GPIO pin where you connected the first DS18B20 data line
pin1 = machine.Pin(4)  # Use the GPIO pin where you connected the second DS18B20 data line
pin2 = machine.Pin(8)  # Use the GPIO pin where you connected the third DS18B20 data line
pin3 = machine.Pin(12)  # Use the GPIO pin where you connected the third DS18B20 data line

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
        for rom in roms:
            temperature = ds.read_temp(rom)
            print(f"Temperature (Device 1 - {rom.hex()}): {temperature:.2f} °C")

        for rom in roms1:
            temperature1 = ds1.read_temp(rom)
            print(f"Temperature (Device 2 - {rom.hex()}): {temperature1:.2f} °C")

        for rom in roms2:
            temperature2 = ds2.read_temp(rom)
            print(f"Temperature (Device 3 - {rom.hex()}): {temperature2:2.2f} °C")

        for rom in roms3:
            temperature3 = ds3.read_temp(rom)
            print(f"Temperature (Device 4 - {rom.hex()}): {temperature3:2.2f} °C")    

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")