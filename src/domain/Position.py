class Position:
    def __init__(self, x_coordinate: int, y_coordinate: int) -> None:
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate

    def __eq__(self, other: {"Position"}) -> bool:
        if not isinstance(other, Position):
            return False

        return (
            self._x_coordinate == other._x_coordinate
            and self._y_coordinate == other._y_coordinate
        )

    def get_x_coordinate(self) -> int:
        return self._x_coordinate

    def get_y_coordinate(self) -> int:
        return self._y_coordinate
