from typing import Dict, Optional, List


from domain.Position import Position
from domain.PriorityQueue import PriorityQueue
from domain.exception.InvalidMazeException import InvalidMazeException
from domain.exception.InvalidDestinationException import InvalidDestinationException
from domain.exception.InvalidStartPointException import InvalidStartPointException
from domain.pathfinding.GridLocation import GridLocation
from domain.pathfinding.IShortestPathAlgorithm import IShortestPathAlgorithm
from domain.pathfinding.Maze import Maze
from domain.pathfinding.Path import Path


class AStarShortestPathAlgorithm(IShortestPathAlgorithm):
    def __init__(self):
        self._maze: Maze = None
        self._size_x = int()
        self._size_y = int()

    def get_dimensions(self) -> tuple:
        return self._maze.get_shape()

    def set_maze(self, maze: Maze):
        self._maze = self._validate_maze(maze)
        self._size_x = self._maze.get_shape()[0]
        self._size_y = self._maze.get_shape()[1]

    def find_shortest_path_with_cartesian_coordinates(
        self, start_position: Position, goal_position: Position
    ):
        start_position = Position(
            start_position.get_y_coordinate(), start_position.get_x_coordinate()
        )
        goal_position = Position(
            goal_position.get_y_coordinate(), goal_position.get_x_coordinate()
        )
        return self._find_shortest_path(start_position, goal_position)

    def _find_shortest_path(self, start_position: Position, goal_position: Position):
        if self._maze is None:
            raise InvalidMazeException

        start = start_position.to_tuple()
        goal = goal_position.to_tuple()
        start_x, start_y = start
        goal_x, goal_y = goal
        size_x, size_y = self.get_dimensions()

        if start_x not in range(0, size_x + 1) or start_y not in range(0, size_y + 1):
            raise InvalidStartPointException
        if goal_x not in range(0, size_x + 1) or goal_y not in range(0, size_y + 1):
            raise InvalidDestinationException
        if self._maze[start_x][start_y] == 1:
            raise InvalidStartPointException
        if self._maze[goal_x][goal_y] == 1:
            raise InvalidDestinationException

        came_from = self._a_star_search(start, goal)
        path = self._reconstruct_path(came_from, start, goal)

        return path

    # A* algorithm with Priority Queue
    # Worst case performance: O(|E|) = O(b^d)
    # Worst case space complexity: O(|V|) = O(b^d)
    # link to pseudocode https://en.wikipedia.org/wiki/A*_search_algorithm
    # other link: https://www.redblobgames.com/pathfinding/a-star/implementation.html
    def _a_star_search(
        self, start: GridLocation, goal: GridLocation, diagonal_movement: bool = False
    ):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from: Dict[GridLocation, Optional[GridLocation]] = dict()
        cost_so_far: Dict[GridLocation, int] = dict()
        came_from[start] = None
        cost_so_far[start] = 0
        cost_of_visiting_one_node = 1
        infinity = 200000

        while not frontier.empty():
            current: GridLocation = frontier.get()

            if current == goal:
                break

            current_x, current_y = current

            if diagonal_movement:
                neighbours = self._find_neighbours_using_diagonal_movements(
                    current_x, current_y
                )
            else:
                neighbours = self._find_neighbours_using_linear_movements(
                    current_x, current_y
                )

            for next_node in neighbours:
                if next_node[0] > self._size_x or next_node[1] > self._size_y:
                    continue
                try:
                    new_cost = (
                        cost_so_far[current]
                        + self._maze[current_x, current_y] * infinity
                        + cost_of_visiting_one_node
                    )
                except IndexError:
                    continue

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self._heuristic(next_node, goal)
                    frontier.put(next_node, priority)
                    came_from[next_node] = current

        return came_from

    def _find_neighbours_using_linear_movements(self, current_x, current_y):
        return {
            (current_x, abs(current_y - 1)),
            (current_x, current_y + 1),
            (abs(current_x - 1), current_y),
            (current_x + 1, current_y),
        }

    def _find_neighbours_using_diagonal_movements(self, current_x, current_y):
        neighbours = {
            (current_x, abs(current_y - 1)),
            (current_x, current_y + 1),
            (abs(current_x - 1), current_y),
            (current_x + 1, current_y),
            (abs(current_x - 1), abs(current_y - 1)),
            (abs(current_x + 1), abs(current_y + 1)),
            (abs(current_x + 1), abs(current_y - 1)),
            (abs(current_x - 1), abs(current_y + 1)),
        }
        return neighbours

    def _reconstruct_path(
        self,
        came_from: Dict[GridLocation, GridLocation],
        start: GridLocation,
        goal: GridLocation,
    ) -> Path:
        current: GridLocation = goal
        path: List[Position] = []
        while current != start:
            current_y_coordinate, current_x_coordinate = current
            path.append(Position(current_x_coordinate, current_y_coordinate))
            current = came_from[current]
        start_y_coordinate, start_x_coordinate = start
        path.append(Position(start_x_coordinate, start_y_coordinate))
        path.reverse()
        return Path(path)

    # eucledian heuristic
    def _heuristic(self, a: GridLocation, b: GridLocation) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def _validate_maze(self, maze: Maze) -> Maze:
        if maze.get_shape() != (0,) and len(maze.get_shape()) <= 2:
            return maze
        raise InvalidMazeException
