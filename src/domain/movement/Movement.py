from domain.movement.Direction import Direction
from domain.movement.Distance import Distance


class Movement:
    def __init__(self, direction: Direction, distance: Distance) -> None:
        self._direction = direction
        self._distance = distance

    def get_direction(self) -> Direction:
        return self._direction

    def get_distance(self) -> Distance:
        return self._distance
