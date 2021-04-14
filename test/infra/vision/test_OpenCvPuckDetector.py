from unittest import TestCase

import cv2

from domain.Position import Position
from domain.Color import Color
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector


class TestOpenCvPuckDetector(TestCase):
    AN_IMAGE_WITH_BLUE_PUCK = cv2.imread("resources/puck-color/image-7.jpg")

    def setUp(self) -> None:
        self.puck_detector = OpenCvPuckDetector()

    def test_givenAnImage_whenDetectBluePuck_thenReturnTheCenterPositionOfTheBluePuck(
        self,
    ):
        expected_position = Position(115, 277)

        actual_position = self.puck_detector.detect(
            self.AN_IMAGE_WITH_BLUE_PUCK, Color.BLUE
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAnImageWithoutTheDesiredPuck_whenDetect_thenRaisePuckNotFoundException(
        self,
    ):
        with self.assertRaises(PuckNotFoundException):
            self.puck_detector.detect(self.AN_IMAGE_WITH_BLUE_PUCK, Color.YELLOW)
