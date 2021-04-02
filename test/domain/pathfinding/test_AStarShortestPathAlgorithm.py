from unittest import TestCase
import numpy as np

from domain.Position import Position
from domain.exception.InvalidMazeException import InvalidMazeException
from domain.exception.InvalidDestinationException import InvalidDestinationException
from domain.exception.InvalidStartPointException import InvalidStartPointException
from domain.pathfinding.AStarShortestPathAlgorithm import AStarShortestPathAlgorithm
from domain.pathfinding.Maze import Maze
from domain.pathfinding.Path import Path


class TestAStarShortestPathAlgorithm(TestCase):
    A_BAD_MAZE = Maze(array=np.array([]))
    A_MAZE = Maze(
        array=np.array(
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
    )
    AN_HORIZONTALLY_OUT_OF_BOUND_POSITION = Position(1, 25)
    A_VERTICALLY_OUT_OF_BOUND_POSITION = Position(12, 1)
    A_NEGATIVE_HORIZONTAL_POSITION = Position(1, -1)
    A_NEGATIVE_VERTICAL_POSITION = Position(-1, 1)
    A_VALID_POSITION = Position(1, 1)
    ANOTHER_VALID_POSITION = Position(2, 2)
    AN_OBSTACLE_POSITION = Position(4, 0)

    def setUp(self) -> None:
        self.a_start_algorithm = AStarShortestPathAlgorithm()
        self.a_start_algorithm.set_maze(self.A_MAZE)

    def test_givenABadMaze_whenInitializingAlgorithm_thenRaiseInvalidMazeException(
        self,
    ):
        algorithm = AStarShortestPathAlgorithm()

        with self.assertRaises(InvalidMazeException):
            algorithm.set_maze(self.A_BAD_MAZE)

    def test_givenNoneMazeSet_whenFindPath_thenRaiseInvalidMazeException(self):
        algorithm = AStarShortestPathAlgorithm()

        with self.assertRaises(InvalidMazeException):
            algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_VALID_POSITION, self.ANOTHER_VALID_POSITION
            )

    def test_givenStartPositionWithNegativeCoordinate_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_NEGATIVE_VERTICAL_POSITION, self.A_VALID_POSITION
            )

    def test_givenHorizontallyOutOfBoundsStartPosition_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.AN_HORIZONTALLY_OUT_OF_BOUND_POSITION, self.A_VALID_POSITION
            )

    def test_givenVerticallyOutOfBoundsStartPosition_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_VERTICALLY_OUT_OF_BOUND_POSITION, self.A_VALID_POSITION
            )

    def test_givenEndPositionWithNegativeCoordinate_whenFindPath_thenRaiseInvalidStartPointException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_NEGATIVE_HORIZONTAL_POSITION, self.A_VALID_POSITION
            )

    def test_givenHorizontallyOutOfBoundsEndingPosition_whenFindPath_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_VALID_POSITION, self.AN_HORIZONTALLY_OUT_OF_BOUND_POSITION
            )

    def test_givenVerticallyOutOfBoundsEndingPosition_whenFindPath_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_VALID_POSITION, self.A_VERTICALLY_OUT_OF_BOUND_POSITION
            )

    def test_givenAMaze_whenFindPathWithObstacleAsDestination_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidDestinationException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.A_VALID_POSITION, self.AN_OBSTACLE_POSITION
            )

    def test_givenAMaze_whenFindPathWithObstacleAsStartPoint_thenRaiseInvalidDestinationException(
        self,
    ):
        with self.assertRaises(InvalidStartPointException):
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                self.AN_OBSTACLE_POSITION, self.A_VALID_POSITION
            )

    def test_givenStartAndEndPosition_whenFindPathWithCartesianCoordinates_thenFlipsCoordinatesAndFindsPath(
        self,
    ):
        starting_position = Position(2, 1)
        ending_position = Position(5, 1)
        expected_path = Path(
            [
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

        actual_path = (
            self.a_start_algorithm.find_shortest_path_with_cartesian_coordinates(
                starting_position, ending_position
            )
        )

        self.assertEqual(expected_path, actual_path)
