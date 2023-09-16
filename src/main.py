from relaycontroller import RelayController
from vhzmeasure import VHZ

if __name__ == '__main__':
      while True:
            print("Voltage: {:.2f} Volts  Frequency: {:.2f} Hz".format(*VHZ.vhzmeasure()))