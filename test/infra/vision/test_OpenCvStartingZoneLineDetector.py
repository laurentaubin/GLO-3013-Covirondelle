from unittest import TestCase

import cv2

from domain.Position import Position
from infra.vision.OpenCvStartingZoneLineDetector import OpenCvStartingZoneLineDetector


class TestOpenCvStartingZoneLineDetector(TestCase):
    AN_IMAGE_WITH_STARTING_ZONE_LINE = cv2.imread(
        "test/infra/vision/resources/image_with_starting_zone_line.jpg"
    )

    def setUp(self) -> None:
        self._starting_zone_line_detector = OpenCvStartingZoneLineDetector()

    def test_givenAnImageWithStartingLineOnIt_whenDetect_thenFindStartingZoneLineCenterPosition(
        self,
    ):
        expected_position: Position = Position(352, 386)

        actual_position = self._starting_zone_line_detector.detect(
            self.AN_IMAGE_WITH_STARTING_ZONE_LINE
        )
        print(actual_position.get_x_coordinate(), actual_position.get_y_coordinate())

        self.assertEqual(actual_position, expected_position)
