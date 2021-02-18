from unittest import TestCase
from unittest.mock import Mock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    def setUp(self):
        self.puck_center_detector = Mock()
        self.starting_zone_corner_detector = Mock()
        self.visionService = VisionService(
            self.puck_center_detector, self.starting_zone_corner_detector
        )
