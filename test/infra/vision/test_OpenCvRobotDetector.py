from unittest import TestCase

import cv2
import cv2.aruco as aruco
from os import path

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from infra.vision.OpenCvRobotDetector import OpenCvRobotDetector


class TestOpenCvRobotDetector(TestCase):
    ARUCO_DICTIONARY = aruco.DICT_4X4_50
    ROBOT_ARUCO_MARKER_ID = 1
    AN_IMAGE = (
        path.dirname(path.abspath(__file__))
        + "/../../../resources/test/robot-detector-test-image-1.jpg"
    )

    def setUp(self) -> None:
        self.robot_detector = OpenCvRobotDetector(
            self.ARUCO_DICTIONARY, self.ROBOT_ARUCO_MARKER_ID
        )

    def test_givenAnImage_whenDetectRobot_thenReturnCorrectRobotPose(self):
        an_image = cv2.imread(self.AN_IMAGE)
        expected_robot_position = Position(719, 663)
        expected_robot_orientation = Orientation(11)
        expected_robot_pose = RobotPose(
            expected_robot_position, expected_robot_orientation
        )

        actual_robot_pose = self.robot_detector.detect(an_image)

        self.assertEqual(expected_robot_pose, actual_robot_pose)
