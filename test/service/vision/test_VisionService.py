from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()
    UNDISTORTED_IMAGE = MagicMock()
    UNDISTORTED_TABLE_IMAGE = MagicMock()

    def setUp(self):
        self.starting_zone_detector = MagicMock()
        self.image_calibrator = MagicMock()
        self.table_detector = MagicMock()
        self.world_camera = MagicMock()
        self.vision_service = VisionService(
            self.starting_zone_detector,
            self.image_calibrator,
            self.table_detector,
            self.world_camera,
        )

    def test_whenFindStartingZone_thenImageIsUndistorted(self):
        self.vision_service.find_starting_zone(self.AN_IMAGE)

        self.image_calibrator.calibrate.assert_called_with(self.AN_IMAGE)

    def test_whenFindStartingZone_thenTableIsDetectedFromUndistortedImage(self):
        self.image_calibrator.calibrate.return_value = self.UNDISTORTED_IMAGE

        self.vision_service.find_starting_zone(self.AN_IMAGE)

        self.table_detector.crop_table.assert_called_with(self.UNDISTORTED_IMAGE)

    def test_whenFindStartingZone_thenStartingZoneDetectorUseUndistortedTableImage(
        self,
    ):
        self.image_calibrator.calibrate.return_value = self.UNDISTORTED_IMAGE
        self.table_detector.crop_table.return_value = self.UNDISTORTED_TABLE_IMAGE

        self.vision_service.find_starting_zone(self.AN_IMAGE)

        self.starting_zone_detector.detect.assert_called_with(
            self.UNDISTORTED_TABLE_IMAGE
        )

    def test_whenFindStartingZone_thenReturnStartingZoneFoundByDetector(self):
        self.starting_zone_detector.detect.return_value = self.A_STARTING_ZONE

        actual_starting_zone = self.vision_service.find_starting_zone(self.AN_IMAGE)

        self.assertEqual(self.A_STARTING_ZONE, actual_starting_zone)

    def test_givenAnImage_whenFindRobotPosition_thenImageIsUndistorted(self):
        self.vision_service.find_robot_position(self.AN_IMAGE)

        self.image_calibrator.calibrate.assert_called_with(self.AN_IMAGE)
