class CommandDuration:
    def __init__(self, duration: float):
        self._duration = duration

    def __eq__(self, other):
        if not isinstance(other, CommandDuration):
            return False
        return self._duration == other._duration

    def __hash__(self):
        return hash(self._duration)

    def get_duration(self) -> float:
        return self._duration
