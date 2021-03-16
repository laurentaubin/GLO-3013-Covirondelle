import time

from domain.game.GameState import GameState
from service.vision.VisionService import VisionService


class VisionWorker:
    def __init__(self, vision_service: VisionService):
        self._vision_service = vision_service

    def run(self):
        while True:
            self.update_vision_state(self._vision_service)
            time.sleep(1)

    @staticmethod
    def update_vision_state(vision_service: VisionService):
        table_image, robot_pose = vision_service.get_vision_state()
        GameState().set_table_image(table_image)
        GameState().set_robot_pose(robot_pose)
