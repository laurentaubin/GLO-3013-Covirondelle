from typing import List

from domain.Position import Position
from domain.StartingZoneCorner import StartingZoneCorner


def take_x_coordinate(position: Position) -> int:
    return position.get_x_coordinate()


def take_y_coordinate(position: Position) -> int:
    return position.get_y_coordinate()


class StartingZone:
    def __init__(
        self, corner_positions: List[Position], starting_zone_center: Position
    ) -> None:
        self._upper_left_corner, self._upper_right_corner = self._find_upper_corners(
            corner_positions
        )
        self._lower_left_corner, self._lower_right_corner = self._find_lower_corners(
            corner_positions
        )
        self._center = starting_zone_center

    def _find_upper_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[:2], key=take_x_coordinate)

    def _find_lower_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[2:4], key=take_x_coordinate)

    def get_center(self):
        return self._center

    def get_corners(self):
        return [
            self._upper_left_corner,
            self._upper_right_corner,
            self._lower_left_corner,
            self._lower_right_corner,
        ]

    def __eq__(self, other: "StartingZone") -> bool:
        if not isinstance(other, StartingZone):
            return False

        return (
            self._upper_left_corner == other._upper_left_corner
            and self._upper_right_corner == other._upper_right_corner
            and self._lower_left_corner == other._lower_left_corner
            and self._lower_right_corner == other._lower_right_corner
            and self._center == other._center
        )

    def find_corner_position_from_letter(
        self, corner_letter: StartingZoneCorner
    ) -> Position:
        starting_zone_letter_to_corner = {
            StartingZoneCorner.A: self._upper_left_corner,
            StartingZoneCorner.B: self._upper_right_corner,
            StartingZoneCorner.C: self._lower_right_corner,
            StartingZoneCorner.D: self._lower_left_corner,
        }

        return starting_zone_letter_to_corner.get(corner_letter)
