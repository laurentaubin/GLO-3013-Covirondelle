from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.exception.InvalidOrientationException import InvalidOrientationException
from domain.movement.Direction import Direction
from domain.movement.Movement import Movement
from domain.movement.MovementFactory import MovementFactory
from domain.pathfinding.Path import Path
from domain.Position import Position
from domain.movement.Distance import Distance


class TestMovementFactory(TestCase):
    A_POSITION = MagicMock()
    ANOTHER_POSITION = MagicMock()
    A_DIRECTION = Direction.FORWARD
    A_DISTANCE = Distance(10)
    AN_ORIENTATION = Orientation(90)

    def setUp(self) -> None:
        self.movement_factory = MovementFactory()

    def test_givenSingleLinePath_whenCreateMovements_thenSingleMovementIsCreated(self):
        a_path = Path([Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 4)])

        movements = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )

        self.assertEqual(1, len(movements))

    def test_givenPathWithNinetyDegreeTurn_whenCreateMovements_thenTwoMovementsAreCreated(
        self,
    ):
        a_path = Path(
            [
                Position(3, 0),
                Position(3, 1),
                Position(3, 2),
                Position(3, 3),
                Position(2, 3),
                Position(1, 3),
                Position(0, 3),
            ]
        )

        movements = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )

        self.assertEqual(2, len(movements))

    def test_givenPathWithNinetyDegreeTurnAndGoingBackwards_whenCreateMovements_thenTwoMovementsAreCreated(
        self,
    ):
        a_path = Path(
            [
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
                Position(1, 0),
                Position(2, 0),
                Position(3, 0),
                Position(4, 0),
            ]
        )

        movements = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )

        self.assertEqual(2, len(movements))

    def test_givenStraightPathWithFivePoints_whenCreateMovements_thenASingleMovementWithDistanceFiveIsCreated(
        self,
    ):
        a_path = Path(
            [
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
                Position(1, 4),
                Position(1, 5),
            ]
        )
        expected_distance = Distance(distance=5)

        movements = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )
        movement_distance = movements[0].get_distance()

        self.assertEqual(expected_distance, movement_distance)

    def test_givenPathWithTurn_whenCreateMovements_thenTwoMovementsWithRightDistancesAreCreated(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
                Position(4, 2),
                Position(4, 3),
                Position(4, 4),
            ]
        )
        expected_first_distance = Distance(distance=4)
        expected_second_distance = Distance(distance=3)

        movements = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )
        first_movement_distance = movements[0].get_distance()
        second_movement_distance = movements[1].get_distance()

        self.assertEqual(expected_first_distance, first_movement_distance)
        self.assertEqual(expected_second_distance, second_movement_distance)

    def test_givenStraightPathWithXIncreasing_whenCreateMovementsWithWestOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
            ]
        )
        forward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )[0]
        self.assertEqual(Direction.FORWARD, forward_movement.get_direction())

    def test_givenStraightPathWithXIncreasing_whenCreateMovementsWithSouthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
            ]
        )
        right_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.SOUTH.value
        )[0]
        self.assertEqual(Direction.RIGHT, right_movement.get_direction())

    def test_givenStraightPathWithXIncreasing_whenCreateMovementsWithNorthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
            ]
        )
        left_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.NORTH.value
        )[0]
        self.assertEqual(Direction.LEFT, left_movement.get_direction())

    def test_givenStraightPathWithXIncreasing_whenCreateMovementsWithEastOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
            ]
        )
        backward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.EAST.value
        )[0]
        self.assertEqual(Direction.BACKWARDS, backward_movement.get_direction())

    def test_givenStraightPathWithXDecreasing_whenCreateMovementsWithWestOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(4, 1),
                Position(3, 1),
                Position(2, 1),
                Position(1, 1),
            ]
        )

        backward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )[0]
        self.assertEqual(Direction.BACKWARDS, backward_movement.get_direction())

    def test_givenStraightPathWithXDecreasing_whenCreateMovementsWithSouthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(4, 1),
                Position(3, 1),
                Position(2, 1),
                Position(1, 1),
            ]
        )
        left_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.SOUTH.value
        )[0]
        self.assertEqual(Direction.LEFT, left_movement.get_direction())

    def test_givenStraightPathWithXDecreasing_whenCreateMovementsWithNorthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(4, 1),
                Position(3, 1),
                Position(2, 1),
                Position(1, 1),
            ]
        )
        right_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.NORTH.value
        )[0]
        self.assertEqual(Direction.RIGHT, right_movement.get_direction())

    def test_givenStraightPathWithXDecreasing_whenCreateMovementsWithEastOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(4, 1),
                Position(3, 1),
                Position(2, 1),
                Position(1, 1),
            ]
        )
        forward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.EAST.value
        )[0]
        self.assertEqual(Direction.FORWARD, forward_movement.get_direction())

    def test_givenStraightPathWithYIncreasing_whenCreateMovementsWithWestOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(1, 2),
                Position(1, 3),
                Position(1, 4),
            ]
        )
        right_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )[0]
        self.assertEqual(Direction.RIGHT, right_movement.get_direction())

    def test_givenStraightPathWithYIncreasing_whenCreateMovementsWithSouthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(1, 2),
                Position(1, 3),
                Position(1, 4),
            ]
        )
        backward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.SOUTH.value
        )[0]
        self.assertEqual(Direction.BACKWARDS, backward_movement.get_direction())

    def test_givenStraightPathWithYIncreasing_whenCreateMovementsWithNorthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(1, 2),
                Position(1, 3),
                Position(1, 4),
            ]
        )
        forward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.NORTH.value
        )[0]
        self.assertEqual(Direction.FORWARD, forward_movement.get_direction())

    def test_givenStraightPathWithYIncreasing_whenCreateMovementsWithEastOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 1),
                Position(1, 2),
                Position(1, 3),
                Position(1, 4),
            ]
        )
        left_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.EAST.value
        )[0]
        self.assertEqual(Direction.LEFT, left_movement.get_direction())

    def test_givenStraightPathWithYDecreasing_whenCreateMovementsWithWestOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )
        left_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.WEST.value
        )[0]
        self.assertEqual(Direction.LEFT, left_movement.get_direction())

    def test_givenStraightPathWithYDecreasing_whenCreateMovementsWithSouthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )
        forward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.SOUTH.value
        )[0]
        self.assertEqual(Direction.FORWARD, forward_movement.get_direction())

    def test_givenStraightPathWithYDecreasing_whenCreateMovementsWithNorthOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )
        backward_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.NORTH.value
        )[0]
        self.assertEqual(Direction.BACKWARDS, backward_movement.get_direction())

    def test_givenStraightPathWithYDecreasing_whenCreateMovementsWithEastOrientation_thenReturnSingleMovementWithCorrectDirection(
        self,
    ):
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )
        right_movement = self.movement_factory.create_movements(
            a_path, CardinalOrientation.EAST.value
        )[0]
        self.assertEqual(Direction.RIGHT, right_movement.get_direction())

    def test_givenOrientationCloseToCardinalOrientationSouth_whenCreateMovements_thenReturnMovementWithRightDirection(
        self,
    ):
        a_close_orientation = Orientation(91)
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )
        expected_direction = Direction.FORWARD

        movement = self.movement_factory.create_movements(a_path, a_close_orientation)[
            0
        ]

        self.assertEqual(movement.get_direction(), expected_direction)

    def test_givenOrientationFarFromCardinalOrientation_whenCreateMovements_thenRaiseInvalidOrientationException(
        self,
    ):
        a_far_orientation = Orientation(188)
        a_path = Path(
            [
                Position(1, 4),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
            ]
        )

        creating_movements = lambda: self.movement_factory.create_movements(
            a_path, a_far_orientation
        )

        with self.assertRaises(InvalidOrientationException):
            creating_movements()

    @patch(
        "infra.utils.GeometryUtils.GeometryUtils.calculate_distance_between_two_positions"
    )
    def test_givenTwoPositions_whenCreateMovementToGetToPointWithDirection_thenCalculateDistanceBetweenTwoPoints(
        self, geometryUtils_mock
    ):
        self.movement_factory.create_movement_to_get_to_point_with_direction(
            self.A_POSITION, self.ANOTHER_POSITION, self.A_DIRECTION
        )

        geometryUtils_mock.assert_called_with(self.A_POSITION, self.ANOTHER_POSITION)

    @patch(
        "infra.utils.GeometryUtils.GeometryUtils.calculate_distance_between_two_positions"
    )
    def test_givenCalculatedDistance_whenCreateMovementToGetToPointWithDirection_returnMovementWithDirectionAndDistance(
        self, geometryUtils_mock
    ):
        geometryUtils_mock.return_value = self.A_DISTANCE
        expected_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)

        actual_movement = (
            self.movement_factory.create_movement_to_get_to_point_with_direction(
                self.A_POSITION, self.ANOTHER_POSITION, self.A_DIRECTION
            )
        )

        self.assertEqual(expected_movement, actual_movement)

    def test_givenPathOfOnePosition_whenCreateMovement_thenReturnSingleMovementPath(
        self,
    ):
        a_one_position_path = Path([Position(0, 0)])

        movements = self.movement_factory.create_movements(
            a_one_position_path, self.AN_ORIENTATION
        )

        self.assertEqual(len(movements), 1)
