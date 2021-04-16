import time

from config.config import STARTING_ZONE_CENTER_POSITION
from domain.CardinalOrientation import CardinalOrientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.game.GameState import GameState
from domain.vision.exception.RobotNotFoundException import RobotNotFoundException
from service.vision.VisionService import VisionService


class VisionWorker:
    last_known_pose = RobotPose(
        Position(STARTING_ZONE_CENTER_POSITION[0], STARTING_ZONE_CENTER_POSITION[1]),
        CardinalOrientation.WEST.value,
    )

    def __init__(self, vision_service: VisionService):
        self._vision_service = vision_service

    def run(self):
        while True:
            self.update_vision_state(self._vision_service)
            time.sleep(0.1)

    @staticmethod
    def update_vision_state(vision_service: VisionService):
        try:
            table_image, robot_pose = vision_service.get_vision_state()
            GameState.get_instance().set_table_image(table_image)
            GameState.get_instance().set_robot_pose(robot_pose)
            VisionWorker.last_known_pose = robot_pose
        except RobotNotFoundException:
            GameState.get_instance().set_robot_pose(VisionWorker.last_known_pose)
