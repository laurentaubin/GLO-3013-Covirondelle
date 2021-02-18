from domain.vision.IPuckCenterDetector import IPuckCenterDetector
from domain.vision.ICornerDetector import ICornerDetector


class VisionService:
    def __init__(
        self,
        puck_center_detector: IPuckCenterDetector,
        starting_zone_corner_detector: ICornerDetector,
    ) -> None:
        self._puck_center_detector = puck_center_detector
        self._starting_zone_corner_detector = starting_zone_corner_detector
