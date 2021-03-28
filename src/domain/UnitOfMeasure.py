from enum import Enum

from config.config import PIXEL_TO_METERS_RATIO


class UnitOfMeasure(Enum):
    PIXEL = PIXEL_TO_METERS_RATIO
    CENTIMETERS = 100
    METER = 1

    def __init__(self, unit_to_meter_ratio: float):
        self._unit_to_meter_ratio = unit_to_meter_ratio

    def get_unit_to_meter_ratio(self) -> float:
        return self._unit_to_meter_ratio
