from typing import Tuple, List

import numpy as np

from domain.Position import Position
from domain.Puck import Puck
from domain.pathfinding.Maze import Maze


class MazeFactory:
    def __init__(self, robot_radius: int, obstacle_radius: int) -> None:
        self._robot_radius = robot_radius
        self._obstacle_radius = obstacle_radius

    def create_from_shape(self, shape: Tuple[int, int, int]) -> Maze:
        width, height, *_ = shape
        array = np.zeros((width, height))
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width - 1 or j == height - 1:
                    array[i][j] = 1

        return Maze(array)

    def create_from_shape_and_obstacles(
        self, shape: Tuple[int, int, int], obstacles: List[Position]
    ):
        maze = self.create_from_shape(shape)
        for obstacle in obstacles:
            maze.add_obstacle(obstacle, self._robot_radius, self._obstacle_radius)

        return maze

    def create_from_shape_and_obstacles_and_pucks_as_obstacles(
        self,
        shape: Tuple[int, int, int],
        obstacles: List[Position],
        pucks: List[Puck],
    ):
        maze = self.create_from_shape(shape)
        for obstacle in obstacles:
            maze.add_obstacle(obstacle, self._robot_radius, self._obstacle_radius)
        for puck in pucks:
            maze.add_puck_as_obstacle(puck.get_position())
        return maze
