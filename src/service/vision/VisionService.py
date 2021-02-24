from domain.Position import Position
from domain.vision.IPuckCenterDetector import IPuckCenterDetector
from domain.vision.ICornerDetector import ICornerDetector
from domain import StartingZone


class VisionService:
    def __init__(
        self,
        puck_center_detector: IPuckCenterDetector,
        starting_zone_corner_detector: ICornerDetector,
    ) -> None:
        # TODO Create class to take pictures of table and pass it here instead of requiring an image in method arguments
        self._puck_center_detector = puck_center_detector
        self._starting_zone_corner_detector = starting_zone_corner_detector

    def find_starting_zone(self, image) -> StartingZone:
        # TODO Make sure image is not null once infra is here
        if not image:
            return None
        return self._starting_zone_corner_detector.detect_starting_zone(image)

    def find_robot_position(self, image) -> Position:
        # TODO
        pass
