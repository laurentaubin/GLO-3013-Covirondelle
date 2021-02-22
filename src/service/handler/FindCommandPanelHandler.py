import time

from domain.game.IStageHandler import IStageHandler


class FindCommandPanelHandler(IStageHandler):
    def __init__(self):
        pass

    def execute(self):
        print("In FindCommandPanelHandler, doing stuff, waiting 3 sec")
        time.sleep(3)
