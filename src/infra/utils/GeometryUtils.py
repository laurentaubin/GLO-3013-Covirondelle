import numpy as np

from domain.Position import Position


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
