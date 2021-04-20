import numpy as np

from domain.Position import Position


class Maze:
    def __init__(self, array: np.array):
        self._array = array

    def get_shape(self):
        return self._array.shape

    def add_obstacle(
        self, obstacle_position: Position, robot_radius: int, obstacle_radius
    ) -> None:
        x_coordinate, y_coordinate = obstacle_position.to_tuple()
        total_obstacle_radius = robot_radius + obstacle_radius

        for i in range(-total_obstacle_radius, total_obstacle_radius + 1):
            for j in range(-total_obstacle_radius, total_obstacle_radius + 1):
                if i + j <= total_obstacle_radius * 2:
                    try:
                        self._array[y_coordinate + i][x_coordinate + j] = 1
                    except IndexError:
                        continue

    def add_puck_as_obstacle(
        self, obstacle_position: Position, robot_radius=0, obstacle_radius=40
    ) -> None:
        x_coordinate, y_coordinate = obstacle_position.to_tuple()
        total_obstacle_radius = robot_radius + obstacle_radius

        for i in range(-total_obstacle_radius, total_obstacle_radius + 1):
            for j in range(-total_obstacle_radius, total_obstacle_radius + 1):
                if i + j <= total_obstacle_radius * 2:
                    try:
                        self._array[y_coordinate + i][x_coordinate + j] = 1
                    except IndexError:
                        continue

    def __getitem__(self, item):
        return self._array[item]

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
