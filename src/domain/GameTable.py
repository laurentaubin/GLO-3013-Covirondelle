from domain.Position import Position
from domain.StartingZone import StartingZone


from domain.pathfinding.Maze import Maze


class GameTable:
    def __init__(
        self, starting_zone: StartingZone, maze: Maze, puck_zone_center: Position
    ):
        self._starting_zone = starting_zone
        self._maze = maze
        self._puck_zone_center = puck_zone_center

    def get_maze(self) -> Maze:
        return self._maze

    def get_starting_zone(self) -> StartingZone:
        return self._starting_zone

    def get_puck_zone_center(self) -> Position:
        return self._puck_zone_center
