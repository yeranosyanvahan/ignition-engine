import smbus

CHANNEL = 0
FILENAME = "data.csv"

# I2C address of the PCF8591
pcf8591_addr = 0x48

# I2C bus number (usually 1 on the Raspberry Pi)
i2c_bus = 1

# Initialize the I2C bus
bus = smbus.SMBus(i2c_bus)

# Function to read the analog voltage from a given channel (0-3)
def read_analog(channel):
    # Send the control byte to the PCF8591
    # 0x40 = enable analog input, single-ended mode
    # 0x40 + channel = select the desired input channel (A0-A3)
    bus.write_byte(pcf8591_addr, 0x40 + channel)

    # return the analog value from the selected channel (0-255)
    return bus.read_byte(pcf8591_addr)


# Read the analog voltage from all 4 channels and print them to the console
import time
with open(FILENAME,'w') as data:
  data.write("Voltage,Time_ms \n")
  data.write('\n'.join([f"{str(read_analog(CHANNEL)).rjust(3,'0')},{time.monotonic_ns()/1000000}" for _ in range(1000)]))
