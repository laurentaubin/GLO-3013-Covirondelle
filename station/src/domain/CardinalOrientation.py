from enum import Enum

from domain.Orientation import Orientation


class CardinalOrientation(Enum):
    WEST = Orientation(0)
    SOUTH = Orientation(90)
    EAST = Orientation(180)
    NORTH = Orientation(270)
