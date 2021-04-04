from typing import List

import numpy as np

from domain.GameTable import GameTable
from domain.Color import Color
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.game.Stage import Stage
from domain.resistance import Resistance


class GameState:
    __instance__ = None

    def __init__(self):
        if GameState.__instance__ is None:
            GameState.__instance__ = self
        else:
            raise Exception("You cannot create another GameState class")
        self._is_started: bool = False
        self._puck_colors: List[Color] = None
        self._current_puck: Color = None
        self._current_stage: Stage = None
        self._prehensor_state: int = None
        self._starting_zone_corner_order: List[StartingZoneCorner] = None
        self._robot_pose: RobotPose = None
        self._table_image: np.array = None
        self._battery_consumption: float = None
        self._game_table: GameTable = None
        self._resistance_value: Resistance = None
        self._current_planned_trajectory: List[Position] = None

    @staticmethod
    def get_instance() -> "GameState":
        if not GameState.__instance__:
            GameState()
        return GameState.__instance__

    def is_game_cycle_started(self) -> bool:
        return self._is_started

    def start_game_cycle(self) -> None:
        self._is_started = True

    def get_puck_colors(self) -> List[Color]:
        return self._puck_colors

    def set_puck_colors(self, puck_colors: List[Color]) -> None:
        self._puck_colors = puck_colors

    def get_current_puck(self) -> Color:
        return self._current_puck

    def set_current_puck(self, current_puck: Color) -> None:
        self._current_puck = current_puck

    def get_current_stage(self) -> Stage:
        return self._current_stage

    def set_current_stage(self, current_stage: Stage) -> None:
        self._current_stage = current_stage

    def get_prehensor_state(self) -> int:
        return self._prehensor_state

    def set_prehensor_state(self, prehensor_state) -> None:
        self._prehensor_state = prehensor_state

    def get_starting_zone_corners(self) -> List[StartingZoneCorner]:
        return self._starting_zone_corner_order

    def get_game_table(self) -> GameTable:
        return self._game_table

    def set_starting_zone_corners(
        self, starting_zone_corners: List[StartingZoneCorner]
    ) -> None:
        self._starting_zone_corner_order = starting_zone_corners

    def get_robot_pose(self) -> RobotPose:
        return self._robot_pose

    def set_robot_pose(self, robot_pose: RobotPose) -> None:
        self._robot_pose = robot_pose

    def get_table_image(self) -> np.ndarray:
        return self._table_image

    def set_table_image(self, table_image: np.ndarray) -> None:
        self._table_image = table_image

    def get_battery_consumption(self):
        return self._battery_consumption

    def set_battery_consumption(self, battery_consumption) -> None:
        self._battery_consumption = battery_consumption

    def set_game_table(self, game_table: GameTable) -> None:
        self._game_table = game_table

    def get_resistance_value(self) -> Resistance:
        return self._resistance_value

    def set_resistance_value(self, value: Resistance):
        self._resistance_value = value

    def get_current_planned_trajectory(self) -> List[Position]:
        return self._current_planned_trajectory

    def set_current_planned_trajectory(
        self, planned_trajectory: List[Position]
    ) -> None:
        self._current_planned_trajectory = planned_trajectory
