class CommandDuration:
    FLOAT_THRESHOLD = 0.0001

    def __init__(self, duration: float):
        self._duration = duration

    def __eq__(self, other):
        if not isinstance(other, CommandDuration):
            return False

        return (
            other._duration - CommandDuration.FLOAT_THRESHOLD
            <= self._duration
            <= other._duration + CommandDuration.FLOAT_THRESHOLD
        )

    def __hash__(self):
        return hash(self._duration)

    def get_duration(self) -> float:
        return self._duration
