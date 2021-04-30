from unittest import TestCase

import cv2
import cv2.aruco as aruco
import numpy as np
from os import path

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from infra.vision.OpenCvRobotDetector import OpenCvRobotDetector


class TestOpenCvRobotDetector(TestCase):
    ARUCO_DICTIONARY = aruco.DICT_4X4_50
    ROBOT_ARUCO_MARKER_ID = 1
    ROBOT_ARUCO_MARKER_SIZE = 0.1
    CALIBRATION_ARRAYS = np.load(
        path.dirname(path.abspath(__file__))
        + "/../../../src/config/numpy-1600x1200.npz"
    )
    CAMERA_MATRIX = CALIBRATION_ARRAYS["camera_matrix"]
    DISTORTION_COEFFICIENTS = CALIBRATION_ARRAYS["distortion_coefficients"]
    ROBOT_HEIGHT = 0.3
    AN_IMAGE = (
        path.dirname(path.abspath(__file__))
        + "/../../../resources/test/robot-detector-test-image-1.jpg"
    )

    def setUp(self) -> None:
        self.robot_detector = OpenCvRobotDetector(
            self.ARUCO_DICTIONARY,
            self.ROBOT_ARUCO_MARKER_ID,
            self.ROBOT_ARUCO_MARKER_SIZE,
            self.CAMERA_MATRIX,
            self.DISTORTION_COEFFICIENTS,
            self.ROBOT_HEIGHT,
        )

    def test_givenAnImage_whenDetectRobot_thenReturnCorrectRobotPose(self):
        an_image = cv2.imread(self.AN_IMAGE)
        expected_robot_position = Position(705, 664)
        expected_robot_orientation = Orientation(11)
        expected_robot_pose = RobotPose(
            expected_robot_position, expected_robot_orientation
        )

        actual_robot_pose = self.robot_detector.detect(an_image)

        self.assertEqual(expected_robot_pose, actual_robot_pose)
