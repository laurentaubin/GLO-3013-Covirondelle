from typing import List

import cv2
import cv2.aruco as aruco
import numpy as np

from config.config import (
    OBSTACLE_ARUCO_MARKER_SIZE,
    OBSTACLE_ARUCO_MARKER_ID,
    CAMERA_MATRIX,
    DISTORTION_COEFFICIENTS,
    OBSTACLE_HEIGHT,
    CALIBRATION_FILE_PATH,
)
from domain.Position import Position
from domain.vision.IObstacleDetector import IObstacleDetector
from domain.vision.exception.ObstacleNotFoundException import ObstacleNotFoundException
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.utils.GeometryUtils import GeometryUtils


# https://github.com/ddelago/Aruco-Marker-Calibration-and-Pose-Estimation/blob/master/pose_marker.py
# https://docs.opencv.org/master/d7/d53/tutorial_py_pose.html


class OpenCvObstacleDetector(IObstacleDetector):
    def __init__(
        self,
        aruco_dictionary,
        obstacle_aruco_marker_id,
        camera_matrix,
        distortion_coefficients,
        aruco_marker_size,
        obstacle_height,
    ):
        self._detector_parameters = aruco.DetectorParameters_create()
        self._aruco_dictionary = aruco.Dictionary_get(aruco_dictionary)
        self._obstacle_aruco_marker_id = obstacle_aruco_marker_id
        self._camera_matrix = camera_matrix
        self._distortion_coefficients = distortion_coefficients
        self._aruco_marker_radius = aruco_marker_size / 2
        self._obstacle_height = obstacle_height

    def detect(self, image: np.ndarray) -> List[Position]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(
            gray,
            self._aruco_dictionary,
            parameters=self._detector_parameters,
            cameraMatrix=self._camera_matrix,
            distCoeff=self._distortion_coefficients,
        )
        all_image_points = self._get_obstacles_aruco_marker_image_points(corners, ids)
        all_obstacle_corners = self._filter_only_obstacle_corners(corners, ids)
        positions = self._get_obstacle_positions_from_projection_points(
            all_obstacle_corners
        )
        projection_points = self._get_projection_points(all_image_points)
        projected_positions = self._get_obstacle_positions_from_projection_points(
            projection_points
        )
        good_position = self._validate_projection(positions, projected_positions)
        return good_position

    def _validate_projection(
        self,
        not_projected_positions: List[Position],
        projected_positions: List[Position],
    ):
        good_positions = []
        for not_projected, projected_position in zip(
            not_projected_positions, projected_positions
        ):
            if (
                500 <= not_projected.get_x_coordinate() <= 800
                and 250 <= not_projected.get_y_coordinate() <= 600
            ):
                good_positions.append(not_projected)
            else:
                if not_projected.get_x_coordinate() <= 630:
                    if (
                        not_projected.get_x_coordinate()
                        > projected_position.get_x_coordinate()
                    ):
                        raise ObstacleNotFoundException()
                elif not_projected.get_x_coordinate() >= 650:
                    if (
                        not_projected.get_x_coordinate()
                        < projected_position.get_x_coordinate()
                    ):
                        raise ObstacleNotFoundException()
                else:
                    if not_projected.get_y_coordinate() < 385:
                        if (
                            not_projected.get_y_coordinate()
                            > projected_position.get_y_coordinate()
                        ):
                            raise ObstacleNotFoundException()
                    elif not_projected.get_y_coordinate() > 415:
                        if (
                            not_projected.get_y_coordinate()
                            < projected_position.get_y_coordinate()
                        ):
                            raise ObstacleNotFoundException()
                good_positions.append(projected_position)
        return good_positions

    def _get_obstacles_aruco_marker_image_points(
        self, corners: List[np.ndarray], ids: List[np.ndarray]
    ) -> List[np.ndarray]:
        all_image_points = []
        all_obstacle_corners = self._filter_only_obstacle_corners(corners, ids)
        for obstacle_corners in all_obstacle_corners:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                obstacle_corners,
                OBSTACLE_ARUCO_MARKER_SIZE,
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
            all_image_points.append(image_points)
        return all_image_points

    def _filter_only_obstacle_corners(
        self, corners: List[np.ndarray], ids: List[np.ndarray]
    ) -> List[np.ndarray]:
        obstacle_corners = []
        if np.all(ids is not None):
            for i, found_id in enumerate(ids):
                if found_id == self._obstacle_aruco_marker_id:
                    obstacle_corners.append(corners[i])
        if len(obstacle_corners) == 0:
            raise ObstacleNotFoundException
        return obstacle_corners

    def _get_projection_axis(self) -> np.ndarray:
        return np.float32(
            [
                [
                    -self._aruco_marker_radius,
                    -self._aruco_marker_radius,
                    -self._obstacle_height,
                ],
                [
                    -self._aruco_marker_radius,
                    self._aruco_marker_radius,
                    -self._obstacle_height,
                ],
                [
                    self._aruco_marker_radius,
                    self._aruco_marker_radius,
                    -self._obstacle_height,
                ],
                [
                    self._aruco_marker_radius,
                    -self._aruco_marker_radius,
                    -self._obstacle_height,
                ],
                [-self._aruco_marker_radius, -self._aruco_marker_radius, 0],
                [-self._aruco_marker_radius, self._aruco_marker_radius, 0],
                [self._aruco_marker_radius, self._aruco_marker_radius, 0],
                [self._aruco_marker_radius, -self._aruco_marker_radius, 0],
            ]
        )

    def _get_projection_points(
        self, all_obstacle_image_points: List[np.ndarray]
    ) -> List[List[np.ndarray]]:
        projection_points = []
        for obstacle_image_points in all_obstacle_image_points:
            reshaped_image_points = np.int32(obstacle_image_points).reshape(-1, 2)
            projection_points.append([reshaped_image_points[:4]])
        return projection_points

    def _get_obstacle_positions_from_projection_points(
        self, all_obstacle_projection_points: List[List[np.ndarray]]
    ) -> List[Position]:
        real_obstacle_positions = []
        for obstacle_projection_points in all_obstacle_projection_points:
            real_obstacle_positions.append(
                self.get_quadrangle_center_coordinates_from_corner_coordinates(
                    obstacle_projection_points[0]
                )
            )
        return real_obstacle_positions

    def get_quadrangle_center_coordinates_from_corner_coordinates(
        self,
        corners: np.ndarray,
    ) -> Position:
        return Position(
            int(self.get_quadrangle_center_x_coordinate_from_corners(corners)),
            int(self.get_quadrangle_center_y_coordinate_from_corners(corners)),
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
