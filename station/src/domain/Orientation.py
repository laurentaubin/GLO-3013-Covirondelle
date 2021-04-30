import math


class Orientation:
    def __init__(self, orientation):
        self._orientation = orientation

    def __eq__(self, other: "Orientation") -> bool:
        if not isinstance(other, Orientation):
            return False

        return self._orientation == other._orientation

    def __sub__(self, other):
        if isinstance(other, Orientation):
            return Orientation(self._orientation - other._orientation)

    def __repr__(self):
        return f"{self._orientation}"

    def get_orientation_in_degree(self) -> int:
        return self._orientation

    def set_orientation(self, orientation: int) -> None:
        self._orientation = orientation

    def get_orientation_in_radians(self) -> float:
        return self._orientation * (math.pi / 180)

    @staticmethod
    def from_radian(angle: float) -> "Orientation":
        return Orientation(int(angle / math.pi * 180))
