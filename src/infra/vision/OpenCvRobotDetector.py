import math

import cv2
import cv2.aruco as aruco

from domain.Orientation import Orientation
from domain.RobotPose import RobotPose
from domain.vision.IRobotDetector import IRobotDetector
from domain.vision.exception import RobotNotFoundException

# https://stackoverflow.com/questions/22780757/how-can-i-get-angle-and-line-length-in-python-opencv
from infra.utils.GeometryUtils import GeometryUtils


class OpenCvRobotDetector(IRobotDetector):
    RAD_TO_DEG_FACTOR = 180 / math.pi

    def __init__(self, aruco_dictionary, robot_aruco_marker_id):
        self._detector_parameters = aruco.DetectorParameters_create()
        self._aruco_dictionary = aruco.Dictionary_get(aruco_dictionary)
        self._robot_aruco_marker_id = robot_aruco_marker_id

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(
            gray, self._aruco_dictionary, parameters=self._detector_parameters
        )

        robot_marker_corners = self._get_robot_marker_corners(corners, ids)
        robot_orientation = Orientation(
            self._get_robot_orientation_in_degree(robot_marker_corners)
        )
        robot_position = (
            GeometryUtils.get_quadrangle_center_coordinates_from_corner_coordinates(
                robot_marker_corners[0]
            )
        )
        return RobotPose(robot_position, robot_orientation)

    def _get_robot_marker_corners(self, corners, ids):
        for i in range(ids.shape[0]):
            if ids[i] == self._robot_aruco_marker_id:
                return corners[i]
        raise RobotNotFoundException

    def _get_robot_orientation_in_degree(self, robot_marker_corner) -> int:
        marker_upper_left_corner = (
            int(robot_marker_corner[0][0][0]),
            int(robot_marker_corner[0][0][1]),
        )
        marker_bottom_left_corner = (
            int(robot_marker_corner[0][3][0]),
            int(robot_marker_corner[0][3][1]),
        )
        orientation = int(
            math.atan2(
                (marker_upper_left_corner[1] - marker_bottom_left_corner[1]),
                (marker_upper_left_corner[0] - marker_bottom_left_corner[0]),
            )
            * self.RAD_TO_DEG_FACTOR
        )
        orientation *= -1
        if orientation < 0:
            orientation = 360 + orientation
        return orientation
