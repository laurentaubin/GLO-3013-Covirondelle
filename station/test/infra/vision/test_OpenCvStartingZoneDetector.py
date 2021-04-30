from unittest import TestCase
import cv2

from domain.Position import Position
from domain.StartingZone import StartingZone


from infra.vision.OpenCvStartingZoneDetector import OpenCvStartingZoneDetector


class TestOpenCvCornerDetector(TestCase):
    AN_IMAGE = "resources/test/startingzone-detector-test-marker-3.jpg"

    def setUp(self) -> None:
        self.detector = OpenCvStartingZoneDetector()

    def test_givenAnImage_whenDetect_thenReturnCorrectStartingZone(self):
        an_image = cv2.imread(self.AN_IMAGE)

        expected_coordinates = [
            Position(195, 814),
            Position(626, 814),
            Position(195, 378),
            Position(626, 378),
        ]
        expected_starting_zone_center = Position(508, 785)
        expected_starting_zone = StartingZone(
            expected_coordinates, expected_starting_zone_center
        )
        actual_starting_zone = self.detector.detect(an_image)
        self.assertEqual(expected_starting_zone, actual_starting_zone)
