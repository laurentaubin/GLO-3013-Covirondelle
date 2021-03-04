from domain.StartingZone import StartingZone
from domain.pathfinding.Maze import Maze


class GameTable:
    def __init__(self, starting_zone: StartingZone, maze: Maze):
        self.starting_zone = starting_zone
        self.maze = maze

    def get_maze(self):
        return self.maze

    def get_starting_zone(self):
        return self.starting_zone
