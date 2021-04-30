# pylint: skip-file
class IServoController:
    def close(self):
        pass

    def sendCmd(self, cmd):
        pass

    def setRange(self, chan, min, max):
        pass

    def getMin(self, chan):
        pass

    def getMax(self, chan):
        pass

    def setTarget(self, chan, target):
        pass

    def setSpeed(self, chan, speed):
        pass

    def setAccel(self, chan, accel):
        pass

    def getPosition(self, chan):
        pass

    def isMoving(self, chan):
        pass

    def getMovingState(self):
        pass

    def runScriptSub(self, subNumber):
        pass

    def stopScript(self):
        pass
