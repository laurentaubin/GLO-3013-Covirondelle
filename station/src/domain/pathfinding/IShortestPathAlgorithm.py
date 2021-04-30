from domain.Position import Position
from domain.pathfinding.Maze import Maze


class IShortestPathAlgorithm:
    def set_maze(self, maze: Maze):
        pass

    def find_shortest_path_with_cartesian_coordinates(
        self, starting_position: Position, ending_position: Position
    ):
        pass
