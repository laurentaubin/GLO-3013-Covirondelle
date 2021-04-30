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
        self._south_east_corner, self._south_west_corner = self._find_west_corners(
            corner_positions
        )
        self._north_east_corner, self._north_west_corner = self._find_north_corners(
            corner_positions
        )
        self._center = starting_zone_center

    def _find_west_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[:2], key=take_x_coordinate)

    def _find_north_corners(self, corner_positions: List[Position]) -> List[Position]:
        corner_positions.sort(key=take_y_coordinate)
        return sorted(corner_positions[2:4], key=take_x_coordinate)

    def get_center(self) -> Position:
        return self._center

    def get_corners(self):
        return [
            self._south_east_corner,
            self._south_west_corner,
            self._north_east_corner,
            self._north_west_corner,
        ]

    def __eq__(self, other: "StartingZone") -> bool:
        if not isinstance(other, StartingZone):
            return False

        return (
            self._south_east_corner == other._south_east_corner
            and self._south_west_corner == other._south_west_corner
            and self._north_east_corner == other._north_east_corner
            and self._north_west_corner == other._north_west_corner
            and self._center == other._center
        )

    def find_corner_position_from_letter(
        self, corner_letter: StartingZoneCorner
    ) -> Position:
        starting_zone_letter_to_corner = {
            StartingZoneCorner.A: self._south_west_corner,
            StartingZoneCorner.B: self._north_west_corner,
            StartingZoneCorner.C: self._north_east_corner,
            StartingZoneCorner.D: self._south_east_corner,
        }

        return starting_zone_letter_to_corner.get(corner_letter)
