from domain import StartingZone
from domain.Position import Position
from domain.camera.ICalibrator import ICalibrator
from domain.vision.IStartingZoneDetector import IStartingZoneDetector


class VisionService:
    def __init__(
        self,
        starting_zone_corner_detector: IStartingZoneDetector,
        calibrator: ICalibrator,
    ) -> None:
        # TODO Create class to take pictures of table and pass it here instead of requiring an image in method arguments
        self._starting_zone_corner_detector = starting_zone_corner_detector
        self._calibrator = calibrator

    def find_starting_zone(self, image) -> StartingZone:
        # TODO Make sure image is not null once infra is here
        if not image:
            return None
        undistorted_image = self._calibrator.calibrate(image)
        return self._starting_zone_corner_detector.detect(undistorted_image)

    def find_robot_position(self, image) -> Position:
        self._calibrator.calibrate(image)
