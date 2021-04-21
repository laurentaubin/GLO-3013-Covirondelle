import time
from typing import List

import cv2
from cv2.aruco import DICT_4X4_50, DICT_6X6_50

from config.config import (
    CALIBRATION_FILE_PATH,
    LAPTOP_CAMERA_INDEX,
    ROBOT_ARUCO_MARKER_ID,
    ROBOT_ARUCO_MARKER_SIZE,
    CAMERA_MATRIX,
    DISTORTION_COEFFICIENTS,
    ROBOT_HEIGHT,
    OBSTACLE_ARUCO_MARKER_ID,
    OBSTACLE_ARUCO_MARKER_SIZE,
    OBSTACLE_HEIGHT,
)
from domain.Color import Color
from domain.Position import Position
from domain.vision.exception.RobotNotFoundException import RobotNotFoundException
from domain.RobotPose import RobotPose
from domain.vision.exception.ObstacleNotFoundException import ObstacleNotFoundException
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera
from infra.vision.OpenCvObstacleDetector import OpenCvObstacleDetector
from infra.vision.OpenCvRobotDetector import OpenCvRobotDetector
from infra.vision.TemplateMatchingPuckDetector import TemplateMatchingPuckDetector

if __name__ == "__main__":
    calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
    camera = OpenCvWorldCamera(LAPTOP_CAMERA_INDEX, calibrator)
    detector = TemplateMatchingPuckDetector()
    robot_detector = OpenCvRobotDetector(
        DICT_4X4_50,
        ROBOT_ARUCO_MARKER_ID,
        ROBOT_ARUCO_MARKER_SIZE,
        CAMERA_MATRIX,
        DISTORTION_COEFFICIENTS,
        ROBOT_HEIGHT,
    )
    obstacle_detector = OpenCvObstacleDetector(
        DICT_4X4_50,
        OBSTACLE_ARUCO_MARKER_ID,
        CAMERA_MATRIX,
        DISTORTION_COEFFICIENTS,
        OBSTACLE_ARUCO_MARKER_SIZE,
        OBSTACLE_HEIGHT,
    )
    should_continue = True
    images = []

    while should_continue:
        image = camera.take_world_image()
        try:
            robot_position: RobotPose = robot_detector.detect(image)
            cv2.circle(
                image,
                robot_position.get_position().to_tuple(),
                15,
                (0, 255, 0),
                10,
            )
        except RobotNotFoundException:
            pass
        try:
            obstacle_positions: List[Position] = obstacle_detector.detect(image)
            for obstacle_position in obstacle_positions:
                print(obstacle_position)
                cv2.circle(
                    image,
                    obstacle_position.to_tuple(),
                    40,
                    (0, 0, 255),
                    10,
                )
                cv2.rectangle(image, (obstacle_position.get_x_coordinate() - 150, obstacle_position.get_y_coordinate() - 150), (obstacle_position.get_x_coordinate()  +150, obstacle_position.get_y_coordinate() + 150), (0, 0, 255), 3)
        except ObstacleNotFoundException:
            print("Robot not found")
            pass

        # for color in Color:
        #     if color is Color.NONE:
        #         continue
        #     position = detector.detect(image, color)
        #     cv2.circle(
        #         image,
        #         position.to_tuple(),
        #         22,
        #         (0, 255, 0),
        #         1,
        #     )
        #     text_position = (
        #         position.get_x_coordinate() - 15,
        #         position.get_y_coordinate() - 40,
        #     )
        #     cv2.putText(
        #         image,
        #         color.name,
        #         text_position,
        #         cv2.FONT_HERSHEY_SIMPLEX,
        #         0.3,
        #         10,
        #     )

        cv2.imshow("image", image)
        k = cv2.waitKey(1)
        if k == 27:  # Esc key to stop
            break
