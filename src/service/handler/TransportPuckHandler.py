import time
from domain.game.IStageHandler import IStageHandler
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class TransportPuckHandler(IStageHandler):
    def __init__(
        self, vision_service: VisionService, movement_service: MovementService
    ):
        self._vision_service: VisionService = vision_service
        self._movement_service: MovementService = movement_service

    def execute(self):
        print("In TransportPuck, doing stuff, waiting 3 sec")
        time.sleep(3)
