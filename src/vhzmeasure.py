import smbus
import numpy as np
import time 

class VHZ:
    CHANNEL = 0

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
        VHZ.bus.write_byte(VHZ.pcf8591_addr, 0x40 + channel)

        # return the analog value from the selected channel (0-255)
        return VHZ.bus.read_byte(VHZ.pcf8591_addr)


    def vhzmeasure(nsample = 1000):
            VT = np.array([(VHZ.read_analog(VHZ.CHANNEL), time.monotonic_ns()//1000) for _ in range(nsample)])

            MILISECOND = 1000
            VOLT = 1.052

            V, T  = VT[5:-5].astype(int).T
            index = np.where( (V[2:] <= V[1:-1]) & (V[1:-1] > V [:-2]))[0]

            if np.all(V < 50) or len(index) < 10:
                return 0,0

            Vind = V[index]*VOLT
            Tind = T[index]

            dT = np.diff(Tind)
            Hz = 1000*MILISECOND / np.average(dT[(dT > 5*MILISECOND) & (dT < 30*MILISECOND)])

            Vlt = np.average(Vind[Vind > 50])
            return Vlt,Hz 

if __name__ == '__main__':
      while True:
            print("Voltage: {:.2f} Volts  Frequency: {:.2f} Hz".format(*VHZ.vhzmeasure()))