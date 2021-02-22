import time
from domain.game.IStageHandler import IStageHandler


class GoParkHandler(IStageHandler):
    def __init__(self):
        pass

    def execute(self):
        print("In GoParkHandler, doing stuff, waiting 3 sec")
        time.sleep(3)
