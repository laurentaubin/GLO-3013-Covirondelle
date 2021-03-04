import numpy as np

from config import config
from domain.Position import Position

ROBOT_RADIUS = config.ROBOT_RADIUS
OBSTACLE_RADIUS = config.OBSTACLE_RADIUS


class Maze:
    def __init__(self, array: np.array = None, width: int = 0, height: int = 0):
        if array is None:
            self.array = self._instantiate_maze(width, height)
        else:
            self.array = array

    def get_shape(self):
        return self.array.shape

    def add_obstacle(self, obstacle_position: Position) -> None:
        x_coordinate, y_coordinate = obstacle_position.to_tuple()
        total_obstacle_radius = ROBOT_RADIUS + OBSTACLE_RADIUS

        for i in range(-total_obstacle_radius, total_obstacle_radius + 1):
            for j in range(-total_obstacle_radius, total_obstacle_radius + 1):
                if i ** 2 + j ** 2 < total_obstacle_radius ** 2:
                    try:
                        self.array[y_coordinate + i][x_coordinate + j] = 1
                    except IndexError:
                        continue

    def _instantiate_maze(self, width: int, height: int) -> np.array:
        array = np.zeros((width, height))
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width - 1 or j == height - 1:
                    array[i][j] = 1

        return array

    def __getitem__(self, item):
        return self.array[item]

    def __eq__(self, other):
        if not isinstance(other, Maze):
            return False

        if not self.get_shape() == other.get_shape():
            return False

        width, height = self.get_shape()

        for i in range(width):
            for j in range(height):
                if self[i][j] != other[i][j]:
                    return False
        return True
