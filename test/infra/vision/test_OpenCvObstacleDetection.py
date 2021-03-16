from unittest import TestCase

import cv2
import cv2.aruco as aruco
import numpy as np

from domain.Position import Position
from domain.vision.exception.ObstacleNotFoundException import ObstacleNotFoundException
from infra.vision.OpenCvObstacleDetector import OpenCvObstacleDetector


class TestOpenCvObstacleDetector(TestCase):
    ARUCO_DICTIONARY = aruco.DICT_4X4_50
    OBSTACLE_ARUCO_MARKER_ID = 0
    OBSTACLE_ARUCO_MARKER_SIZE = 0.08
    OBSTACLE_HEIGHT = 0.304
    AN_IMAGE = cv2.imread("resources/test/obstacle-detector-test-image-1.jpg")
    AN_IMAGE_WITH_OBSTACLE_WITHOUT_ARUCO_MARKER = cv2.imread(
        "resources/test/obstacle_detector_no_marker_test.png"
    )
    CALIBRATION_ARRAYS = np.load("src/config/numpy-1600x1200.npz")
    CAMERA_MATRIX = CALIBRATION_ARRAYS["camera_matrix"]
    DISTORTION_COEFFICIENTS = CALIBRATION_ARRAYS["distortion_coefficients"]

    def setUp(self) -> None:
        self.obstacle_detector = OpenCvObstacleDetector(
            self.ARUCO_DICTIONARY,
            self.OBSTACLE_ARUCO_MARKER_ID,
            self.CAMERA_MATRIX,
            self.DISTORTION_COEFFICIENTS,
            self.OBSTACLE_ARUCO_MARKER_SIZE,
            self.OBSTACLE_HEIGHT,
        )

    def test_givenAnImageWithTwoObstacles_whenDetectObstacle_thenReturnCorrectObstaclePosition(
        self,
    ):
        expected_first_obstacle_position, expected_second_obstacle_position = [
            Position(1100, 757),
            Position(787, 311),
        ]

        actual_obstacle_position = self.obstacle_detector.detect(self.AN_IMAGE)

        self.assertEqual(expected_first_obstacle_position, actual_obstacle_position[0])
        self.assertEqual(expected_second_obstacle_position, actual_obstacle_position[1])

    def test_givenAnImageWithObstaclesWithoutArucoMarker_whenDetect_thenRaiseObstacleNotFoundException(
        self,
    ):
        detecting_obstacles = lambda image: self.obstacle_detector.detect(image)

        self.assertRaises(
            ObstacleNotFoundException,
            detecting_obstacles,
            self.AN_IMAGE_WITH_OBSTACLE_WITHOUT_ARUCO_MARKER,
        )
