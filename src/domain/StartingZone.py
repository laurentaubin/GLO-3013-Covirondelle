from typing import List

from domain.Position import Position


def take_x_coordinate(position: Position) -> int:
    return position.get_x_coordinate()


def take_y_coordinate(position: Position) -> int:
    return position.get_y_coordinate()


class StartingZone:
    def __init__(self, corner_positions: List[Position]) -> None:
        self._upper_left_corner, self._upper_right_corner = self._find_upper_corners(
            corner_positions
        )
        self._lower_left_corner, self._lower_right_corner = self._find_lower_corners(
            corner_positions
        )

    def _find_upper_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[:2], key=take_x_coordinate)

    def _find_lower_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[2:4], key=take_x_coordinate)

    def __eq__(self, other: {"StartingZone"}) -> bool:
        if not isinstance(other, StartingZone):
            return False

        return (
            self._upper_left_corner == other._upper_left_corner
            and self._upper_right_corner == other._upper_right_corner
            and self._lower_left_corner == other._lower_left_corner
            and self._lower_right_corner == other._lower_right_corner
        )
