from unittest import TestCase
import cv2

from domain.Color import Color
from domain.Position import Position
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector


class TestOpenCvPuckDetector(TestCase):
    AN_IMAGE = "resources/test/puck-detector-test-marker-3.jpg"

    def setUp(self) -> None:
        self.detector = OpenCvPuckDetector()

    def test_givenAnImageAndPuckColor_whenDetect_thenDetectThePuckCenter(self):
        an_image = cv2.imread(self.AN_IMAGE)
        expected_puck_center = Position(1471, 303)

        actual_puck_center = self.detector.detect(an_image, Color.BLACK)

        self.assertEqual(expected_puck_center, actual_puck_center)
