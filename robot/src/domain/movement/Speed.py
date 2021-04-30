from domain.movement.CommandDuration import CommandDuration
from domain.movement.Distance import Distance


class Speed:
    def __init__(self, speed: float):
        self._speed = speed

    def get_speed(self) -> float:
        return self._speed

    def __lt__(self, other: "Speed") -> bool:
        return self._speed < other._speed

    def __mul__(self, other: float) -> float:
        return self._speed * other

    def __eq__(self, other):
        if not isinstance(other, Speed):
            return False

        return self._speed == other._speed

    @staticmethod
    def calculate_from_distance_and_duration(
        distance: Distance, duration: CommandDuration
    ) -> "Speed":
        return Speed(distance.get_distance() / duration.get_duration())
