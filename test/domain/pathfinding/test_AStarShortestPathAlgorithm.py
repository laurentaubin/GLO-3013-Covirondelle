from unittest import TestCase
import numpy as np

from domain.Position import Position
from domain.exception.InvalidMazeException import InvalidMazeException
from domain.exception.InvalidDestinationException import InvalidDestinationException
from domain.exception.InvalidStartPointException import InvalidStartPointException
from domain.pathfinding.AStarShortestPathAlgorithm import AStarShortestPathAlgorithm
from domain.pathfinding.Path import Path


class TestAStarShortestPathAlgorithm(TestCase):
    A_BAD_MAZE = np.array([])
    A_MAZE = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    )
    AN_HORIZONTALLY_OUT_OF_BOUND_POSITION = Position(25, 1)
    A_VERTICALLY_OUT_OF_BOUND_POSITION = Position(1, 12)
    A_NEGATIVE_HORIZONTAL_POSITION = Position(-1, 1)
    A_NEGATIVE_VERTICAL_POSITION = Position(1, -1)
    A_VALID_POSITION = Position(1, 1)
    AN_OBSTACLE_POSITION = Position(0, 4)

    def setUp(self) -> None:
        self.a_start_algorithm = AStarShortestPathAlgorithm(self.A_MAZE)

    def test_givenABadMaze_whenInitializingAlgorithm_thenRaiseInvalidBoardException(
        self,
    ):
        with self.assertRaises(InvalidMazeException):
            AStarShortestPathAlgorithm(self.A_BAD_MAZE)

    def test_givenStartPositionWithNegativeCoordinate_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path(
                self.A_NEGATIVE_VERTICAL_POSITION, self.A_VALID_POSITION
            )

    def test_givenHorizontallyOutOfBoundsStartPosition_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path(
                self.AN_HORIZONTALLY_OUT_OF_BOUND_POSITION, self.A_VALID_POSITION
            )

    def test_givenVerticallyOutOfBoundsStartPosition_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path(
                self.A_VERTICALLY_OUT_OF_BOUND_POSITION, self.A_VALID_POSITION
            )

    def test_givenEndPositionWithNegativeCoordinate_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path(
                self.A_NEGATIVE_HORIZONTAL_POSITION, self.A_VALID_POSITION
            )

    def test_givenHorizontallyOutOfBoundsEndingPosition_whenFindPath_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path(
                self.A_VALID_POSITION, self.AN_HORIZONTALLY_OUT_OF_BOUND_POSITION
            )

    def test_givenVerticallyOutOfBoundsEndingPosition_whenFindPath_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path(
                self.A_VALID_POSITION, self.A_VERTICALLY_OUT_OF_BOUND_POSITION
            )

    def test_givenAMaze_whenFindPathWithObstacleAsDestination_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path(
                self.A_VALID_POSITION, self.AN_OBSTACLE_POSITION
            )

    def test_givenAMaze_whenFindPathWithObstacleAsStartPoint_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path(
                self.AN_OBSTACLE_POSITION, self.A_VALID_POSITION
            )

    def test_givenAMaze_whenGetPath_thenReturnCorrectPath(self):
        starting_position = Position(1, 1)
        ending_position = Position(1, 5)
        expected_path = Path(
            [
                Position(1, 1),
                Position(1, 2),
                Position(1, 3),
                Position(2, 3),
                Position(3, 3),
                Position(4, 3),
                Position(5, 3),
                Position(6, 3),
                Position(6, 4),
                Position(6, 5),
                Position(5, 5),
                Position(4, 5),
                Position(3, 5),
                Position(2, 5),
                Position(1, 5),
            ]
        )

        actual_path = self.a_start_algorithm.find_shortest_path(
            starting_position, ending_position
        )

        self.assertEqual(expected_path, actual_path)
