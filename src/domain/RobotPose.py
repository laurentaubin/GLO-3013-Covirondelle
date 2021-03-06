from domain.Orientation import Orientation
from domain.Position import Position


class RobotPose:
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
