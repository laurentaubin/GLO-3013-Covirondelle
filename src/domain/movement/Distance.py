class Distance:
    def __init__(self, distance: float):
        self._distance = distance

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return False

        return self._distance == other._distance

    def get_distance(self) -> float:
        return self._distance
