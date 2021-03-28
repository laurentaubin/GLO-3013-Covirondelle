from domain.UnitOfMeasure import UnitOfMeasure


class Distance:
    def __init__(self, distance: float, unit_of_measure=UnitOfMeasure.PIXEL):
        self._distance = distance / unit_of_measure.get_unit_to_meter_ratio()

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return False

        return self._distance == other._distance

    def get_distance(self) -> float:
        return self._distance
