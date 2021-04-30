from typing import List

from domain.Position import Position
from domain.exception.PositionNotAdjacentException import PositionNotAdjacentException


class Path:
    def __init__(self, path: List[Position]) -> None:
        self._path = path

    def __eq__(self, other):
        if isinstance(other, Path):
            return self._path == other._path
        return False

    def __getitem__(self, item) -> Position:
        return self._path[item]

    def __len__(self) -> int:
        return len(self._path)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._path):
            result = self._path[self.n]
            self.n += 1
            return result
        raise StopIteration

    def add(self, position: Position) -> None:
        if self._position_is_not_adjacent(position):
            raise PositionNotAdjacentException
        self._path.append(position)

    def _position_is_not_adjacent(self, position: Position):
        if len(self) < 1:
            return False

        path_last_position = self[-1]
        are_positions_adjacent_in_x = (
            abs(position.get_x_coordinate() - path_last_position.get_x_coordinate())
            == 1
        )
        are_positions_adjacent_in_y = (
            abs(position.get_y_coordinate() - path_last_position.get_y_coordinate())
            == 1
        )

        return not are_positions_adjacent_in_x != are_positions_adjacent_in_y
