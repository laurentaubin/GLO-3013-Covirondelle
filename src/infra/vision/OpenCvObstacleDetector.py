from typing import List

import cv2
import cv2.aruco as aruco
import numpy as np

from config.config import OBSTACLE_ARUCO_MARKER_SIZE
from domain.Position import Position
from domain.vision.IObstacleDetector import IObstacleDetector
from domain.vision.exception.ObstacleNotFoundException import ObstacleNotFoundException
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

    def detect(self, image: List[np.ndarray]) -> List[Position]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(
            gray,
            self._aruco_dictionary,
            parameters=self._detector_parameters,
            cameraMatrix=self._camera_matrix,
            distCoeff=self._distortion_coefficients,
        )
        all_image_points = self._get_obstacles_aruco_marker_image_points(corners, ids)

        projection_points = self._get_projection_points(all_image_points)
        return self._get_obstacle_positions_from_projection_points(projection_points)

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
                GeometryUtils.get_quadrangle_center_coordinates_from_corner_coordinates(
                    obstacle_projection_points[0]
                )
            )
        return real_obstacle_positions
