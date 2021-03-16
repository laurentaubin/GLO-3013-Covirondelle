from unittest import TestCase

import numpy as np

from domain.Position import Position
from infra.utils.GeometryUtils import GeometryUtils


class TestGeometryUtils(TestCase):
    FIRST_CORNER_COORDINATE = np.array([432, 4])
    SECOND_CORNER_COORDINATE = np.array([54, 975])
    THIRD_CORNER_COORDINATE = np.array([320, 430])
    FOURTH_CORNER_COORDINATE = np.array([202, 103])

    def test_givenQuadrangleCorners_whenGetQuadrangleCenterPositionFromCornersCoordinates_thenReturnCenterPosition(
        self,
    ):
        quadrangle_corners = np.array(
            [
                self.FIRST_CORNER_COORDINATE,
                self.SECOND_CORNER_COORDINATE,
                self.THIRD_CORNER_COORDINATE,
                self.FOURTH_CORNER_COORDINATE,
            ]
        )
        expected_center_coordinates = Position(252, 378)

        actual_center_coordinates = (
            GeometryUtils.get_quadrangle_center_coordinates_from_corner_coordinates(
                quadrangle_corners
            )
        )

        print(actual_center_coordinates)

        self.assertEqual(actual_center_coordinates, expected_center_coordinates)
