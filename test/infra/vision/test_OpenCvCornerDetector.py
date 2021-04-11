from unittest import TestCase

import cv2

from domain.Position import Position
from infra.vision.OpenCvCornerDetector import OpenCvCornerDetector


class TestOpenCvCornerDetector(TestCase):
    IMAGE_1 = cv2.imread("resources/robot-corners-alignment/image-1.jpg")
    IMAGE_2 = cv2.imread("resources/robot-corners-alignment/image-2.jpg")
    IMAGE_3 = cv2.imread("resources/robot-corners-alignment/image-3.jpg")
    IMAGE_4 = cv2.imread("resources/robot-corners-alignment/image-4.jpg")
    IMAGE_5 = cv2.imread("resources/robot-corners-alignment/image-5.jpg")
    IMAGE_6 = cv2.imread("resources/robot-corners-alignment/image-6.jpg")
    IMAGE_7 = cv2.imread("resources/robot-corners-alignment/image-8.jpg")
    IMAGE_8 = cv2.imread("resources/robot-corners-alignment/image-9.jpg")
    IMAGE_9 = cv2.imread("resources/robot-corners-alignment/image-10.jpg")

    def setUp(self) -> None:
        self._detector = OpenCvCornerDetector()

    def test_givenImage1_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(311, 154)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_1)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage2_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(341, 162)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_2)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage3_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(331, 145)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_3)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage4_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(335, 167)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_4)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage5_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(297, 150)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_5)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage6_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(314, 193)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_6)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage7_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(351, 84)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_7)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage8_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(347, 97)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_8)

        self.assertEqual(actual_position, expected_position)

    def test_givenImage9_whenDetectInferiorCorner_thenReturnInferiorCornerPosition(
        self,
    ):
        expected_position = Position(326, 145)

        actual_position = self._detector.detect_inferior_corner(self.IMAGE_9)

        self.assertEqual(actual_position, expected_position)
