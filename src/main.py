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
                  # cancy miacats
                  controller.off('podsos')
                  controller.off('onoff')
                  controller.off('starter')
                  controller.off('ongen')

            elif isenginerunning():
                  # xodats
                  controller.off('starter')
                  controller.off('podsos')
                  controller.on('onoff')
                  controller.on('ongen')
            else:
                  # xodelu 2/10 sec
                  controller.on('starter')
                  controller.on('podsos')
                  controller.on('onoff')
                  controller.off('ongen')
                  time.sleep(2)
                  controller.off('starter')
                  time.sleep(10)

                  