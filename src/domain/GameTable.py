from typing import List

from domain.Color import Color
from domain.Position import Position
from domain.Puck import Puck
from domain.StartingZone import StartingZone

from domain.pathfinding.Maze import Maze


class GameTable:
    def __init__(
        self,
        starting_zone: StartingZone,
        maze: Maze,
        puck_zone_center: Position,
        pucks: List[Puck],
    ):
        self._starting_zone = starting_zone
        self._maze = maze
        self._puck_zone_center = puck_zone_center
        self._pucks = pucks

    def get_maze(self) -> Maze:
        return self._maze

    def get_starting_zone(self) -> StartingZone:
        return self._starting_zone

    def get_puck_zone_center(self) -> Position:
        return self._puck_zone_center

    def get_pucks(self) -> List[Puck]:
        return self._pucks

    def get_puck(self, color: Color) -> Puck:
        for puck in self._pucks:
            if puck.get_color() == color:
                return puck
