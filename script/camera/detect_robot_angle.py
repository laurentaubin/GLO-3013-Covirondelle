import cv2
from cv2.aruco import DICT_4X4_50

from config.config import (
    CALIBRATION_FILE_PATH,
    LAPTOP_CAMERA_INDEX,
    ROBOT_ARUCO_MARKER_ID,
)
from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera
from infra.vision.OpenCvRobotDetector import OpenCvRobotDetector

calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
camera = OpenCvWorldCamera(LAPTOP_CAMERA_INDEX, calibrator)
robot_detector = OpenCvRobotDetector(DICT_4X4_50, ROBOT_ARUCO_MARKER_ID)

if __name__ == "__main__":
    while True:
        image = camera.take_world_image()
        robot_pose = RobotPose(Position(800, 600), Orientation(0))
        try:
            robot_pose = robot_detector.detect(image)
        except:
            pass
        x, y = robot_pose.get_position().to_tuple()

        cv2.putText(
            image,
            str(robot_pose.get_orientation_in_degree().get_orientation_in_degree()),
            (x + 100, y + 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            20,
        )

        cv2.imshow("robot", image)
        cv2.waitKey(1)
