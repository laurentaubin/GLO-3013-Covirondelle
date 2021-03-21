from config.config import PIXEL_TO_CENTIMETERS
from domain.UnitOfMeasure import UnitOfMeasure
from domain.exception.InvalidPositionException import InvalidPositionException


class Position:
    def __init__(
        self,
        x_coordinate: int,
        y_coordinate: int,
        unit_of_measure: UnitOfMeasure = UnitOfMeasure.PIXEL,
    ) -> None:
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._unit_of_measure = unit_of_measure

    def get_x_coordinate(self):
        return self._x_coordinate

    def get_y_coordinate(self):
        return self._y_coordinate

    def get_unit_of_measure(self):
        return self._unit_of_measure

    def to_tuple(self):
        return self._x_coordinate, self._y_coordinate

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False

        if self._unit_of_measure is other.get_unit_of_measure():
            return (
                self._x_coordinate == other._x_coordinate
                and self._y_coordinate == other._y_coordinate
            )
        if self._unit_of_measure is UnitOfMeasure.PIXEL:
            return (
                self._x_coordinate == other._x_coordinate * PIXEL_TO_CENTIMETERS
                and self._y_coordinate == other._y_coordinate * PIXEL_TO_CENTIMETERS
            )
        return (
            self._x_coordinate == other._x_coordinate / PIXEL_TO_CENTIMETERS
            and self._y_coordinate == other._y_coordinate / PIXEL_TO_CENTIMETERS
        )

    def __sub__(self, other):
        if isinstance(other, Position):
            if self._unit_of_measure is other.get_unit_of_measure():
                return Position(
                    self._x_coordinate - other._x_coordinate,
                    self._y_coordinate - other._y_coordinate,
                )
            if self._unit_of_measure is UnitOfMeasure.PIXEL:
                return Position(
                    self._x_coordinate - other._x_coordinate * PIXEL_TO_CENTIMETERS,
                    self._y_coordinate - other._y_coordinate * PIXEL_TO_CENTIMETERS,
                    UnitOfMeasure.PIXEL,
                )
            return Position(
                self._x_coordinate * PIXEL_TO_CENTIMETERS - other._x_coordinate,
                self._y_coordinate * PIXEL_TO_CENTIMETERS - other._y_coordinate,
                UnitOfMeasure.PIXEL,
            )
        raise InvalidPositionException

    def __add__(self, other):
        if isinstance(other, Position):
            if self._unit_of_measure is other.get_unit_of_measure():
                return Position(
                    self._x_coordinate + other._x_coordinate,
                    self._y_coordinate + other._y_coordinate,
                )
            if self._unit_of_measure is UnitOfMeasure.PIXEL:
                return Position(
                    self._x_coordinate + other._x_coordinate * PIXEL_TO_CENTIMETERS,
                    self._y_coordinate + other._y_coordinate * PIXEL_TO_CENTIMETERS,
                    UnitOfMeasure.PIXEL,
                )
            return Position(
                self._x_coordinate * PIXEL_TO_CENTIMETERS + other._x_coordinate,
                self._y_coordinate * PIXEL_TO_CENTIMETERS + other._y_coordinate,
                UnitOfMeasure.PIXEL,
            )
        raise InvalidPositionException

    def __abs__(self):
        return Position(abs(self._x_coordinate), abs(self._y_coordinate))
