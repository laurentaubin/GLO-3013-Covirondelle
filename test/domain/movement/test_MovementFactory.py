from unittest import TestCase

from domain.movement.Direction import Direction
from domain.movement.MovementFactory import MovementFactory
from domain.pathfinding.Path import Path
from domain.Position import Position
from domain.movement.Distance import Distance


class TestMovementFactory(TestCase):
    def setUp(self) -> None:
        self.movement_factory = MovementFactory()

    def test_givenSingleLinePath_whenCreateMovements_thenSingleMovementIsCreated(self):
        a_path = Path([Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 4)])

        movements = self.movement_factory.create_movements(a_path)

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

        movements = self.movement_factory.create_movements(a_path)

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

        movements = self.movement_factory.create_movements(a_path)

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

        movements = self.movement_factory.create_movements(a_path)
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

        movements = self.movement_factory.create_movements(a_path)
        first_movement_distance = movements[0].get_distance()
        second_movement_distance = movements[1].get_distance()

        self.assertEqual(expected_first_distance, first_movement_distance)
        self.assertEqual(expected_second_distance, second_movement_distance)

    def test_givenStraightPathWithXIncreasing_whenCreateMovements_thenReturnSingleMovementWithDirectionForward(
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

        movement = self.movement_factory.create_movements(a_path)[0]

        self.assertEqual(Direction.FORWARD, movement.get_direction())

    def test_givenStraightPathWithXDecreasing_whenCreateMovements_thenReturnSingleMovementWithDirectionBackwards(
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

        movement = self.movement_factory.create_movements(a_path)[0]

        self.assertEqual(Direction.BACKWARDS, movement.get_direction())

    def test_givenStraightPathWithYIncreasing_whenCreateMovements_thenReturnSingleMovementWithDirectionRight(
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

        movement = self.movement_factory.create_movements(a_path)[0]

        self.assertEqual(Direction.RIGHT, movement.get_direction())

    def test_givenStraightPathWithYDecreasing_whenCreateMovements_thenReturnSingleMovementWithDirectionLeft(
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

        movement = self.movement_factory.create_movements(a_path)[0]

        self.assertEqual(Direction.LEFT, movement.get_direction())
