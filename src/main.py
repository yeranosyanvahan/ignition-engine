import time
from relaycontroller import RelayController
from vhzmeasure import VHZ

def isenginerunning():
      Vmin, Vmax = [200,300]
      Hzmin,Hzmax = [40,60]

      V, Hz = VHZ.vhzmeasure()

      if V < Vmin or V > Vmax: return False
      if Hz < Hzmin or Hz > Hzmax: return False

      return True


def isgridon():
      CHANNEL = 1
      SAMPLE = 100

      tmp = [VHZ.read_analog(CHANNEL) for _ in range(SAMPLE)]

      return sum(tmp) > 127*SAMPLE

if __name__ == '__main__':
      controller = RelayController()
      while True:
            print("EngineStatus: %r, GridStatus: %r" % (isenginerunning(), isgridon()))
            if isgridon():
                  controller.off('relay1')
                  controller.off('relay2')
                  controller.off('relay3')
                  controller.off('relay4')
            elif isenginerunning():
                  controller.on('relay1')
                  controller.off('relay2')
                  controller.on('relay3')
                  controller.on('relay4')
            else:
                  controller.on('relay1')
                  controller.on('relay2')
                  controller.off('relay3')
                  controller.off('relay4')
                  time.sleep(2)
                  controller.off('relay1')
                  time.sleep(10)

                  