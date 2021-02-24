from enum import Enum


class StartingZoneCorner(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @staticmethod
    def get_next_corner(current_corner: "StartingZoneCorner") -> "StartingZoneCorner":
        next_corner = {
            StartingZoneCorner.A: StartingZoneCorner.B,
            StartingZoneCorner.B: StartingZoneCorner.C,
            StartingZoneCorner.C: StartingZoneCorner.D,
            StartingZoneCorner.D: StartingZoneCorner.A,
        }
        return next_corner.get(current_corner)
