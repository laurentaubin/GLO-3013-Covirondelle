from domain import StartingZone
from domain.Position import Position
from domain.camera.ICalibrator import ICalibrator
from domain.camera.IWorldCamera import IWorldCamera
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from domain.vision.ITableDetector import ITableDetector


class VisionService:
    def __init__(
        self,
        starting_zone_corner_detector: IStartingZoneDetector,
        calibrator: ICalibrator,
        table_detector: ITableDetector,
        world_camera: IWorldCamera,
    ) -> None:
        # TODO Create class to take pictures of table and pass it here instead of requiring an image in method arguments
        self._starting_zone_corner_detector = starting_zone_corner_detector
        self._calibrator = calibrator
        self._table_detector = table_detector
        self._world_camera = world_camera
        self._world_image = world_camera.take_world_image()

    def find_starting_zone(self, image) -> StartingZone:
        # TODO Make sure image is not null once infra is here
        if not image:
            return None
        table_image = self._get_calibrated_table_image(image)
        return self._starting_zone_corner_detector.detect(table_image)

    def find_robot_position(self, image) -> Position:
        self._calibrator.calibrate(image)

    def _get_calibrated_table_image(self, image):
        undistorted_image = self._calibrator.calibrate(image)
        return self._table_detector.crop_table(undistorted_image)
