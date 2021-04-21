from unittest import TestCase

import numpy as np

from domain.Position import Position
from domain.pathfinding.Maze import Maze
from domain.pathfinding.MazeFactory import MazeFactory


class TestMaze(TestCase):
    A_ROBOT_RADIUS = 2
    AN_OBSTACLE_RADIUS = 3

    A_MAZE_ARRAY = np.array(
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        ]
    )
    AN_INDEX = 2

    def setUp(self) -> None:
        self.maze_factory = MazeFactory(self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS)
        self.maze = Maze(self.A_MAZE_ARRAY)

    def test_whenGetShape_thenReturnNumpyShape(self) -> None:
        expected_shape = self.A_MAZE_ARRAY.shape

        actual_shape = self.maze.get_shape()

        self.assertEqual(expected_shape, actual_shape)

    def test_whenGetItem_thenReturnItemInNumpyArray(self) -> None:
        expected_item = self.A_MAZE_ARRAY[self.AN_INDEX][self.AN_INDEX]

        actual_item = self.maze[self.AN_INDEX][self.AN_INDEX]

        self.assertEqual(expected_item, actual_item)

    def test_givenEmptyMazeAndRobotRadius_whenAddObstacle_thenRobotRadiusIsTakenIntoAccountWhenAddingObstacle(
        self,
    ):
        expected_maze = Maze(
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
            )
        )
        obstacle_position = Position(13, 9)
        actual_maze = self.maze_factory.create_from_shape((17, 20, 0))

        actual_maze.add_obstacle(
            obstacle_position, self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS
        )

        self.assertEqual(expected_maze, actual_maze)

    def test_givenObstacleCloseToEdge_whenAddObstacle_thenDontRaiseIndexOufOfBoundsException(
        self,
    ):
        expected_maze = Maze(
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
            )
        )

        obstacle_position = Position(6, 8)
        actual_maze = self.maze_factory.create_from_shape((8, 10, 0))
        actual_maze.add_obstacle(
            obstacle_position, self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS
        )

        self.assertEqual(expected_maze, actual_maze)

    def test_givenPuckObstacle_whenRemovePuckAsObstacle_thenObstacleIsRemove(self):
        expected_maze = self.maze_factory.create_from_shape((8, 10, 0))
        actual_maze = Maze(
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
            )
        )

        actual_maze.remove_puck_as_obstacle(Position(5, 4), obstacle_radius=2)

        self.assertEqual(actual_maze, expected_maze)
