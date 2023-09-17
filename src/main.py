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

class Controller:
      def __init__(self, relaycontroller):
            self.relaycontroller = relaycontroller
            self.on = relaycontroller.on
            self.off = relaycontroller.off
      
      def genopengrid(self):
            self.relaycontroller.off('starter')
            self.relaycontroller.off('podsos')
            self.relaycontroller.on('onoff')
            self.relaycontroller.on('ongen')

      def killengine(self):
            self.relaycontroller.off('starter')
            self.relaycontroller.off('podsos')
            self.relaycontroller.off('onoff')
            self.relaycontroller.off('ongen')

      def startengine(self):
            self.relaycontroller.on('starter')
            self.relaycontroller.on('podsos')
            self.relaycontroller.on('onoff')
            self.relaycontroller.off('ongen')
            time.sleep(2)
            self.relaycontroller.off('starter')

class WatchLoop:
      TIME_LATENCY_TO_KILL_ENGINE = 10
      TIME_LATENCY_TO_START_ENGINE = 3

      TIME_START_TO_START_ENGINE = 10
      TIME_START_ENGINE_TO_OPEN_GRID = 10

      TIME_LATENCY_TO_OPEN_PODSOS = 1

      def __init__(self, controller: Controller):
            self.controller = controller

            self.lasttime = {
                  "startengine": 0, # inuse
                  "genopengrid": 0,

                  "enginetrue": 0,
                  "enginefalse": 0,

                  "gridfalse": 0, #inuse
                  "gridtrue": 0
            }

      def tick(self, gridstatus, enginestatus):
            self.lasttime['gridtrue' if gridstatus else 'gridfalse'] = time.time()
            self.lasttime['enginetrue' if enginestatus else 'enginefalse'] = time.time()

            if gridstatus and \
               self.lasttime['gridfalse'] + WatchLoop.TIME_LATENCY_TO_KILL_ENGINE < time.time():
                  self.controller.killengine()
                 
            
            if not gridstatus and enginestatus \
                  and self.lasttime['enginetrue'] + WatchLoop.TIME_LATENCY_TO_OPEN_PODSOS:
               self.controller.off('podsos')

               if self.lasttime['enginefalse'] + WatchLoop.TIME_START_ENGINE_TO_OPEN_GRID < time.time():                  
                  self.controller.genopengrid()

            if not gridstatus and not enginestatus:
               if self.lasttime['startengine'] + WatchLoop.TIME_START_TO_START_ENGINE < time.time() and \
                  self.lasttime['gridtrue'] + WatchLoop.TIME_LATENCY_TO_START_ENGINE < time.time():
                  self.controller.startengine()
                  self.lasttime['startengine'] = time.time()
            


if __name__ == '__main__':
      loop = WatchLoop(Controller(RelayController()))
      while True:

            gridstatus = isgridon()
            enginestatus = isenginerunning()

            print("GridStatus: %r, EngineStatus: %r" % (gridstatus, enginestatus))

            try:
                  loop.tick(gridstatus, enginestatus)

            except OSError as e:
                  if "[Errno 121]" in str(e) and "Remote I/O error" in str(e):
                        print("Power Issue")
                  else:
                       print(f"OSError occured: {e}")
                  time.sleep(2)


                  