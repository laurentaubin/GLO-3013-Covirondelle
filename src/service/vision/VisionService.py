from domain.Position import Position
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from domain import StartingZone


class VisionService:
    def __init__(self, starting_zone_detector: IStartingZoneDetector) -> None:
        # TODO Create class to take pictures of table and pass it here instead of requiring an image in method arguments
        self._starting_zone_detector = starting_zone_detector

    def find_starting_zone(self, image) -> StartingZone:
        # TODO Make sure image is not null once infra is here
        if not image:
            return None
        return self._starting_zone_detector.detect(image)

    def find_robot_position(self, image) -> Position:
        # TODO
        pass
