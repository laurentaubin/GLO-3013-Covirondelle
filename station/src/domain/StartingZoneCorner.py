from enum import Enum

from domain.Orientation import Orientation


class StartingZoneCorner(Enum):
    A = Orientation(45)
    B = Orientation(315)
    C = Orientation(225)
    D = Orientation(125)

    @staticmethod
    def get_next_corner(current_corner: "StartingZoneCorner") -> "StartingZoneCorner":
        next_corner = {
            StartingZoneCorner.A: StartingZoneCorner.B,
            StartingZoneCorner.B: StartingZoneCorner.C,
            StartingZoneCorner.C: StartingZoneCorner.D,
            StartingZoneCorner.D: StartingZoneCorner.A,
        }
        return next_corner.get(current_corner)

    @staticmethod
    def value_of_string(string: str) -> "StartingZoneCorner":
        for corner in StartingZoneCorner:
            if corner.name == string:
                return corner
