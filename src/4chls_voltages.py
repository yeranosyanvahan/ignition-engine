import smbus

# I2C address of the PCF8591
pcf8591_addr = 0x48

# I2C bus number (usually 1 on the Raspberry Pi)
i2c_bus = 1

# Initialize the I2C bus
bus = smbus.SMBus(i2c_bus)

# Function to read the analog voltage from a given channel (0-3)
def read_voltage(channel):
    # Send the control byte to the PCF8591
    # 0x40 = enable analog input, single-ended mode
    # 0x40 + channel = select the desired input channel (A0-A3)
    bus.write_byte(pcf8591_addr, 0x40 + channel)

    # Read the analog value from the selected channel (0-255)
    analog_value = bus.read_byte(pcf8591_addr)

    # Convert the analog value to a voltage (0-5V)
    voltage = analog_value / 255.0 * 5.0

    return voltage

# Read the analog voltage from all 4 channels and print them to the console
while True:
    voltages = [read_voltage(i) for i in range(2)]
    
    print("Analog voltages: {:.2f} V, {:.2f} V, {:.2f} V, {:.2f} V".format(*voltages))
