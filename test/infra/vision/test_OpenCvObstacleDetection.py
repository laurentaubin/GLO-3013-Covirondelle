from unittest import TestCase

import cv2
import cv2.aruco as aruco

from domain.Position import Position
from infra.vision.OpenCvObstacleDetector import OpenCvObstacleDetector


class TestOpenCvObstacleDetector(TestCase):
    ARUCO_DICTIONARY = aruco.DICT_4X4_50
    OBSTACLE_ARUCO_MARKER_ID = 0
    AN_IMAGE = "resources/test/obstacle-detector-test-image-1.jpg"

    def setUp(self) -> None:
        self.obstacle_detector = OpenCvObstacleDetector(
            self.ARUCO_DICTIONARY, self.OBSTACLE_ARUCO_MARKER_ID
        )

    def test_givenAnImageWithTwoObstacles_whenDetectObstacle_thenReturnCorrectObstaclePosition(
        self,
    ):
        an_image = cv2.imread(self.AN_IMAGE)
        expected_first_obstacle_position, expected_second_obstacle_position = [
            Position(1156, 805),
            Position(803, 252),
        ]

        actual_obstacle_position = self.obstacle_detector.detect(an_image)

        self.assertEqual(expected_first_obstacle_position, actual_obstacle_position[0])
        self.assertEqual(expected_second_obstacle_position, actual_obstacle_position[1])
