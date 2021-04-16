from config.config import GRIPPER_OFFSET
from domain.Orientation import Orientation
from domain.Position import Position
import numpy as np


class RobotPose:
    GRIPPER_POSE = GRIPPER_OFFSET

    def __init__(self, position: Position, orientation: Orientation):
        self._position = position
        self._orientation_in_degree = orientation

    def __eq__(self, other: "RobotPose") -> bool:
        if not isinstance(other, RobotPose):
            return False

        return (
            self._position == other._position
            and self._orientation_in_degree == other._orientation_in_degree
        )

    def get_position(self):
        return self._position

    def get_orientation_in_degree(self):
        return self._orientation_in_degree

    def get_gripper_position(self):
        gripper_position_x = (
            self._position.get_x_coordinate()
            + np.cos(self._orientation_in_degree.get_orientation_in_radians())
            * self.GRIPPER_POSE
        )
        gripper_position_y = (
            self._position.get_y_coordinate()
            - np.sin(self._orientation_in_degree.get_orientation_in_radians())
            * self.GRIPPER_POSE
        )

        return Position(round(gripper_position_x), round(gripper_position_y))
