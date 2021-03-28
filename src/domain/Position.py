from domain.exception.InvalidPositionException import InvalidPositionException


class Position:
    def __init__(
        self,
        x_coordinate: int,
        y_coordinate: int,
    ) -> None:
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate

    def get_x_coordinate(self):
        return self._x_coordinate

    def get_y_coordinate(self):
        return self._y_coordinate

    def to_tuple(self):
        return self._x_coordinate, self._y_coordinate

    def to_dictionary(self):
        return {"x_coordinate": self._x_coordinate, "y_coordinate": self._y_coordinate}

    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False

        return (
            self._x_coordinate == other._x_coordinate
            and self._y_coordinate == other._y_coordinate
        )

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(
                self._x_coordinate - other._x_coordinate,
                self._y_coordinate - other._y_coordinate,
            )

        raise InvalidPositionException

    def __add__(self, other):
        if isinstance(other, Position):

            return Position(
                self._x_coordinate + other._x_coordinate,
                self._y_coordinate + other._y_coordinate,
            )

        raise InvalidPositionException

    def __abs__(self):
        return Position(abs(self._x_coordinate), abs(self._y_coordinate))
