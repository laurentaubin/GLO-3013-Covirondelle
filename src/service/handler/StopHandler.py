import time
from domain.game.IStageHandler import IStageHandler


class StopHandler(IStageHandler):
    def __init__(self):
        pass

    def execute(self):
        print("In StopHandler, doing stuff, waiting 3 sec")
        print("Turn on the LED")
        time.sleep(3)
