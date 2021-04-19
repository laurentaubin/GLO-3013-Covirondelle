import math
from typing import List

import cv2
import cv2.aruco as aruco
import numpy as np

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.vision.IRobotDetector import IRobotDetector
from domain.vision.exception.RobotNotFoundException import RobotNotFoundException

# https://stackoverflow.com/questions/22780757/how-can-i-get-angle-and-line-length-in-python-opencv
from infra.utils.GeometryUtils import GeometryUtils


class OpenCvRobotDetector(IRobotDetector):
    RAD_TO_DEG_FACTOR = 180 / math.pi

    def __init__(
        self,
        aruco_dictionary,
        robot_aruco_marker_id: int,
        robot_aruco_marker_size: float,
        camera_matrix,
        distortion_coefficients,
        robot_height,
    ):
        self._detector_parameters = aruco.DetectorParameters_create()
        self._aruco_dictionary = aruco.Dictionary_get(aruco_dictionary)
        self._robot_aruco_marker_id = robot_aruco_marker_id
        self._aruco_marker_size = robot_aruco_marker_size
        self._aruco_marker_radius = robot_aruco_marker_size / 2
        self._camera_matrix = camera_matrix
        self._distortion_coefficients = distortion_coefficients
        self._robot_height = robot_height

    def detect(self, image) -> RobotPose:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(
            gray, self._aruco_dictionary, parameters=self._detector_parameters
        )
        robot_marker_corners = self._get_robot_marker_corners(corners, ids)
        marker_position = (
            self.get_quadrangle_center_coordinates_from_corner_coordinates(
                robot_marker_corners[0].reshape(-1, 2)
            )
        )
        robot_marker_image_points = self._get_robot_image_points(robot_marker_corners)
        projection_points = self._get_projection_points(robot_marker_image_points)
        robot_orientation = self._get_robot_orientation_in_degree(robot_marker_corners)
        robot_position = self.get_quadrangle_center_coordinates_from_corner_coordinates(
            projection_points[0]
        )
        if marker_position.get_x_coordinate() < 640:
            if marker_position.get_x_coordinate() > robot_position.get_x_coordinate():
                raise RobotNotFoundException()
        else:
            if marker_position.get_x_coordinate() < robot_position.get_x_coordinate():
                raise RobotNotFoundException()
        return RobotPose(robot_position, robot_orientation)

    def _get_robot_marker_corners(self, corners, ids):
        for i in range(ids.shape[0]):
            if ids[i] == self._robot_aruco_marker_id:
                return corners[i]
        raise RobotNotFoundException

    def _get_robot_image_points(self, corners: List[np.ndarray]):
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
            corners,
            self._aruco_marker_size,
            self._camera_matrix,
            self._distortion_coefficients,
        )
        (rvec - tvec).any()
        axis = self._get_projection_axis()
        image_points, _ = cv2.projectPoints(
            axis,
            rvec,
            tvec,
            self._camera_matrix,
            self._distortion_coefficients,
        )
        return image_points

    def _get_projection_axis(self) -> np.ndarray:
        return np.float32(
            [
                [
                    -self._aruco_marker_radius,
                    -self._aruco_marker_radius,
                    -self._robot_height,
                ],
                [
                    -self._aruco_marker_radius,
                    self._aruco_marker_radius,
                    -self._robot_height,
                ],
                [
                    self._aruco_marker_radius,
                    self._aruco_marker_radius,
                    -self._robot_height,
                ],
                [
                    self._aruco_marker_radius,
                    -self._aruco_marker_radius,
                    -self._robot_height,
                ],
                [-self._aruco_marker_radius, -self._aruco_marker_radius, 0],
                [-self._aruco_marker_radius, self._aruco_marker_radius, 0],
                [self._aruco_marker_radius, self._aruco_marker_radius, 0],
                [self._aruco_marker_radius, -self._aruco_marker_radius, 0],
            ]
        )

    def _get_projection_points(
        self, marker_image_points: List[np.ndarray]
    ) -> List[np.ndarray]:
        reshaped_image_points = np.int32(marker_image_points).reshape(-1, 2)
        return [reshaped_image_points[:4]]

    def _get_robot_orientation_in_degree(self, robot_marker_corner) -> Orientation:
        marker_upper_left_corner = Position(
            int(robot_marker_corner[0][0][0]),
            int(robot_marker_corner[0][0][1]),
        )
        marker_bottom_left_corner = Position(
            int(robot_marker_corner[0][3][0]),
            int(robot_marker_corner[0][3][1]),
        )

        return self.calculate_angle_between_positions(
            marker_bottom_left_corner, marker_upper_left_corner
        )

    def get_quadrangle_center_coordinates_from_corner_coordinates(
        self,
        corners: np.ndarray,
    ) -> Position:
        return Position(
            int(GeometryUtils.get_quadrangle_center_x_coordinate_from_corners(corners)),
            int(GeometryUtils.get_quadrangle_center_y_coordinate_from_corners(corners)),
        )

    def get_quadrangle_center_x_coordinate_from_corners(
        self,
        corners: np.ndarray,
    ) -> np.float64:
        return (corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) / 4

    def get_quadrangle_center_y_coordinate_from_corners(
        self,
        corners: np.ndarray,
    ) -> np.float64:
        return (corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) / 4

    def calculate_angle_between_positions(
        self, first_position: Position, second_position: Position
    ) -> Orientation:
        first_x, first_y = first_position.to_tuple()
        second_x, second_y = second_position.to_tuple()

        angle = -math.atan2(second_y - first_y, second_x - first_x)

        if angle < 0:
            angle += 2 * math.pi

        return Orientation.from_radian(angle)
