from unittest import TestCase

import numpy as np

from domain.Orientation import Orientation
from domain.Position import Position
from domain.movement.Distance import Distance
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

    def test_givenPerpendicularPositions_whenCalculateAngleBetweenPositions_thenReturnOrientationOf90(
        self,
    ):
        first_position = Position(150, 200)
        second_position = Position(150, 150)
        expected_orientation = Orientation(90)

        actual_orientation = GeometryUtils.calculate_angle_between_positions(
            first_position, second_position
        )

        self.assertEqual(expected_orientation, actual_orientation)

    def test_givenPositionsWithAngleOfNegative315Degrees_whenCalculateAngleBetweenPositions_thenReturnOrientationOf315(
        self,
    ):
        first_position = Position(100, 200)
        second_position = Position(150, 250)
        expected_orientation = Orientation(315)

        actual_orientation = GeometryUtils.calculate_angle_between_positions(
            first_position, second_position
        )

        self.assertEqual(expected_orientation, actual_orientation)

    def test_givenPositionsWithDistanceOf5_whenCalculateDistanceBetweenTwoPoints_thenReturnDistanceOf5(
        self,
    ):
        first_position = Position(100, 105)
        second_position = Position(100, 100)
        expected_distance = Distance(5)

        actual_distance = GeometryUtils.calculate_distance_between_two_positions(
            first_position, second_position
        )

        self.assertEqual(actual_distance, expected_distance)
