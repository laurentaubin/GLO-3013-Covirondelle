import time
from domain.game.IStageHandler import IStageHandler


class TransportPuckHandler(IStageHandler):
    def __init__(self):
        pass

    def execute(self):
        print("In TransportPuck, doing stuff, waiting 3 sec")
        time.sleep(3)
