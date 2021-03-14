from unittest import TestCase
from unittest.mock import patch

import numpy as np

from domain.Position import Position
from domain.pathfinding.Maze import Maze


@patch("domain.pathfinding.Maze.ROBOT_RADIUS", 3)
@patch("domain.pathfinding.Maze.OBSTACLE_RADIUS", 2)
class TestMaze(TestCase):
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
        self.maze = Maze(self.A_MAZE_ARRAY)

    def test_whenGetShape_thenReturnNumpyShape(self) -> None:
        expected_shape = self.A_MAZE_ARRAY.shape

        actual_shape = self.maze.get_shape()

        self.assertEqual(expected_shape, actual_shape)

    def test_whenGetItem_thenReturnItemInNumpyArray(self) -> None:
        expected_item = self.A_MAZE_ARRAY[self.AN_INDEX][self.AN_INDEX]

        actual_item = self.maze[self.AN_INDEX][self.AN_INDEX]

        self.assertEqual(expected_item, actual_item)

    def test_whenInstantiatingMazeWithHeightAndWidth_thenMazeHasBorderOfOnes(
            self,
    ):
        maze_width = 5
        maze_height = 10
        expected_maze = Maze(
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                ]
            )
        )

        maze = Maze(width=maze_width, height=maze_height)
        self.assertEqual(maze, expected_maze)

    def test_givenEmptyMazeAndRobotRadius_whenAddObstacle_thenRobotRadiusIsTakenIntoAccountWhenAddingObstacle(
            self,
    ):
        expected_maze = Maze(
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, ],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ], ]
            )
        )
        obstacle_position = Position(13, 9)
        actual_maze = Maze(width=17, height=20)

        actual_maze.add_obstacle(obstacle_position)

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
        actual_maze = Maze(width=8, height=10)

        actual_maze.add_obstacle(obstacle_position)
        self.assertEqual(expected_maze, actual_maze)
