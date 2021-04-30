from unittest import TestCase
from unittest.mock import MagicMock, patch

import numpy as np

from domain.Position import Position
from domain.pathfinding.Maze import Maze
from domain.pathfinding.MazeFactory import MazeFactory


class TestMazeFactory(TestCase):
    A_ROBOT_RADIUS = 2
    AN_OBSTACLE_RADIUS = 3
    SOME_OBSTACLES = [Position(1, 1), Position(4, 4)]
    A_MAZE = MagicMock()
    A_SHAPE = (10, 10, 10)

    def setUp(self) -> None:
        self.maze_factory = MazeFactory(self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS)

    def test_whenCreateFromShape_thenMazeHasBorderOfOnesAndRightShape(
        self,
    ):
        maze_width = 5
        maze_height = 10
        shape = (maze_width, maze_height, 0)
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

        maze = self.maze_factory.create_from_shape(shape)

        self.assertEqual(maze, expected_maze)

    @patch("domain.pathfinding.MazeFactory.MazeFactory.create_from_shape")
    def test_whenCreateFromShapeAndObstacles_thenMazeHasObstaclesAdded(
        self, createFromShape_mock
    ):
        createFromShape_mock.return_value = self.A_MAZE

        self.maze_factory.create_from_shape_and_obstacles(
            self.A_SHAPE, self.SOME_OBSTACLES
        )

        self.A_MAZE.add_obstacle.assert_any_call(
            self.SOME_OBSTACLES[0], self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS
        )
        self.A_MAZE.add_obstacle.assert_any_call(
            self.SOME_OBSTACLES[1], self.A_ROBOT_RADIUS, self.AN_OBSTACLE_RADIUS
        )
