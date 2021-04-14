from config.config import STARTING_ZONE_CORNERS_POSITION, STARTING_ZONE_CENTER_POSITION
from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.vision.IStartingZoneDetector import IStartingZoneDetector


class HardcodedStartingZoneDetector(IStartingZoneDetector):
    def detect(self, image) -> StartingZone:
        corner_positions = [Position(x, y) for x, y in STARTING_ZONE_CORNERS_POSITION]
        center_position = Position(
            STARTING_ZONE_CENTER_POSITION[0], STARTING_ZONE_CENTER_POSITION[1]
        )
        return StartingZone(corner_positions, center_position)
