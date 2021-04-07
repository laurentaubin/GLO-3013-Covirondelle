from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.vision.IStartingZoneDetector import IStartingZoneDetector


class HardcodedStartingZoneDetector(IStartingZoneDetector):
    def detect(self, image) -> StartingZone:
        corner_positions = [
            Position(619, 389),
            Position(611, 809),
            Position(201, 803),
            Position(207, 393),
        ]
        center_position = Position(402, 597)
        return StartingZone(corner_positions, center_position)
