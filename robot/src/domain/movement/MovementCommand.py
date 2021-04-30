from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Speed import Speed


class MovementCommand:
    def __init__(self, direction: Direction, speed: Speed, duration: CommandDuration):
        self._direction = direction
        self._speed = speed
        self._duration = duration

    def __eq__(self, other):
        if not isinstance(other, MovementCommand):
            return False
        return (
            self._direction == other._direction
            and self._speed == other._speed
            and self._duration == other._duration
        )

    def get_direction(self) -> Direction:
        return self._direction

    def get_speed(self) -> Speed:
        return self._speed

    def get_duration(self) -> CommandDuration:
        return self._duration

    def __repr__(self):
        return str((self._direction, self._speed))
