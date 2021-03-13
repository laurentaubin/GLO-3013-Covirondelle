from typing import List

import cv2

import cv2.aruco as aruco

from domain.Position import Position
from domain.vision.IObstacleDetector import IObstacleDetector
from domain.vision.exception import ObstacleNotFoundException


class OpenCvObstacleDetector(IObstacleDetector):
    def __init__(self, aruco_dictionary, obstacle_aruco_marker_id):
        self._detector_parameters = aruco.DetectorParameters_create()
        self._aruco_dictionary = aruco.Dictionary_get(aruco_dictionary)
        self._obstacle_aruco_marker_id = obstacle_aruco_marker_id

    def detect(self, image) -> List[Position]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(
            gray, self._aruco_dictionary, parameters=self._detector_parameters
        )

        obstacle_positions = []
        obstacle_marker_corners = self._get_obstacle_marker_corners(corners, ids)

        for obstacle_marker in obstacle_marker_corners:
            center_x, center_y = self._get_marker_center_in_pixel(obstacle_marker[1])
            position = Position(int(center_x), int(center_y))
            obstacle_positions.append(position)

        return obstacle_positions

    def _get_obstacle_marker_corners(self, corners, ids):
        obs_positions = []
        for i in range(ids.shape[0]):
            if ids[i] == self._obstacle_aruco_marker_id:
                obs_positions.append((ids[i], corners[i]))
        if len(obs_positions) != 0:
            return obs_positions

        raise ObstacleNotFoundException

    def _get_marker_center_in_pixel(self, marker_corner):
        x_center = (
            marker_corner[0][0][0]
            + marker_corner[0][1][0]
            + marker_corner[0][2][0]
            + marker_corner[0][3][0]
        ) / 4
        y_center = (
            marker_corner[0][0][1]
            + marker_corner[0][1][1]
            + marker_corner[0][2][1]
            + marker_corner[0][3][1]
        ) / 4
        return x_center, y_center
