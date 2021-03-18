from typing import List

import numpy as np

from domain.GameTable import GameTable
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.ResistanceColor import ResistanceColor
from domain.game.Stage import Stage


class GameState:
    _instance = None

    def __init__(self):
        self._puck_colors: List[ResistanceColor]
        self._current_puck: ResistanceColor
        self._current_stage: Stage
        self._prehensor_state: int
        self._starting_zone_corner_order: List[StartingZoneCorner]
        self._robot_pose: RobotPose
        self._table_image: np.array
        self._battery_consumption: float
        self._game_table: GameTable

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_puck_colors(self) -> List[ResistanceColor]:
        return self._puck_colors

    def set_puck_colors(self, puck_colors: List[ResistanceColor]):
        self._puck_colors = puck_colors

    def get_current_puck(self) -> ResistanceColor:
        return self._current_puck

    def set_current_puck(self, current_puck: ResistanceColor) -> None:
        self._current_stage = current_puck

    def get_current_stage(self) -> Stage:
        return self._current_stage

    def set_current_stage(self, current_stage: Stage) -> None:
        self._current_stage = current_stage

    def get_prehensor_state(self):
        return self._prehensor_state

    def set_prehensor_state(self, prehensor_state) -> None:
        self._prehensor_state = prehensor_state

    def get_starting_zone_corners(self) -> List[StartingZoneCorner]:
        return self._starting_zone_corner_order

    def get_game_table(self) -> GameTable:
        return self._game_table

    def set_starting_zone_corners(
        self, starting_zone_corners: List[StartingZoneCorner]
    ):
        self._starting_zone_corner_order = starting_zone_corners

    def get_robot_pose(self) -> RobotPose:
        return self._robot_pose

    def set_robot_pose(self, robot_pose: RobotPose) -> None:
        self._robot_pose = robot_pose

    def get_table_image(self):
        return self._table_image

    def set_table_image(self, table_image):
        self._table_image = table_image

    def get_battery_consumption(self):
        return self._battery_consumption

    def set_battery_consumption(self, battery_consumption):
        self._battery_consumption = battery_consumption

    def set_game_table(self, game_table: GameTable):
        self._game_table = game_table
