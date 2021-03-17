from domain.GameTable import GameTable
from domain.Position import Position
from domain.StartingZoneCorner import StartingZoneCorner
from domain.pathfinding.IShortestPathAlgorithm import IShortestPathAlgorithm
from domain.pathfinding.Path import Path


class PathService:
    def __init__(
        self,
        shortest_path_algorithm: IShortestPathAlgorithm,
    ) -> None:
        self._game_table = None
        self._shortest_path_algorithm = shortest_path_algorithm
        self._current_corner_letter = None

    def find_path_to_next_starting_zone_corner(
        self, current_robot_position: Position
    ) -> Path:
        corner_position = (
            self._game_table.get_starting_zone().find_corner_position_from_letter(
                self._current_corner_letter
            )
        )

        self._current_corner_letter = StartingZoneCorner.get_next_corner(
            self._current_corner_letter
        )

        return self._shortest_path_algorithm.find_shortest_path(
            current_robot_position, corner_position
        )

    def set_game_table(self, game_table: GameTable) -> None:
        self._game_table = game_table
        self._shortest_path_algorithm.set_maze(self._game_table.get_maze())

    def set_first_corner_letter(self, corner_letter: StartingZoneCorner):
        self._current_corner_letter = corner_letter
