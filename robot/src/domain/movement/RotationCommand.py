from domain.movement.Direction import Direction


class RotationCommand:
    def __init__(self, direction: Direction, angle: float):
        self._direction = direction
        self._angle = angle

    def get_direction(self) -> Direction:
        return self._direction

    def get_angle(self) -> float:
        return self._angle
