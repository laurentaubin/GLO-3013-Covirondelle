from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()

    def setUp(self):
        self.puck_center_detector = MagicMock()
        self.starting_zone_corner_detector = MagicMock()
        self.vision_service = VisionService(
            self.puck_center_detector, self.starting_zone_corner_detector
        )

    def test_whenFindStartingZone_thenReturnStartingZoneFoundByDetector(self):
        self.starting_zone_corner_detector.detect_starting_zone.return_value = (
            self.A_STARTING_ZONE
        )

        actual_starting_zone = self.vision_service.find_starting_zone(self.AN_IMAGE)

        self.assertEqual(self.A_STARTING_ZONE, actual_starting_zone)
