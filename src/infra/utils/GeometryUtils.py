import numpy as np
import math

from domain.Orientation import Orientation
from domain.Position import Position
from domain.movement.Distance import Distance


class GeometryUtils:
    @staticmethod
    def get_quadrangle_center_coordinates_from_corner_coordinates(
        corners: np.ndarray,
    ) -> Position:
        return Position(
            int(GeometryUtils.get_quadrangle_center_x_coordinate_from_corners(corners)),
            int(GeometryUtils.get_quadrangle_center_y_coordinate_from_corners(corners)),
        )

    @staticmethod
    def get_quadrangle_center_x_coordinate_from_corners(
        corners: np.ndarray,
    ) -> np.float64:
        return (corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) / 4

    @staticmethod
    def get_quadrangle_center_y_coordinate_from_corners(
        corners: np.ndarray,
    ) -> np.float64:
        return (corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) / 4

    @staticmethod
    def calculate_angle_between_positions(
        first_position: Position, second_position: Position
    ) -> Orientation:
        first_x, first_y = first_position.to_tuple()
        second_x, second_y = second_position.to_tuple()

        angle = -math.atan2(second_y - first_y, second_x - first_x)

        if angle < 0:
            angle += 2 * math.pi

        return Orientation.from_radian(angle)

    @staticmethod
    def calculate_distance_between_two_positions(
        first_position: Position, second_position: Position
    ):
        first_x, first_y = first_position.to_tuple()
        second_x, second_y = second_position.to_tuple()

        distance = math.sqrt((first_x - second_x) ** 2 + (first_y - second_y) ** 2)

        return Distance(distance)
