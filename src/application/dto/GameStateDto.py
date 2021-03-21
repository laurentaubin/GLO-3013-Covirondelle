from typing import List

import numpy as np

from domain.Position import Position
from domain.ResistanceColor import ResistanceColor
from domain.StartingZoneCorner import StartingZoneCorner
from domain.game.Stage import Stage


class GameStateDto:
    def __init__(
        self,
        puck_colors: List[str],
        current_puck: str,
        current_stage: str,
        gripper_state: int,
        starting_zone_corner_order: List[str],
        robot_position: dict,
        encoded_table_image: str,
        battery_consumption: float,
    ):
        self._puck_colors: List[str] = puck_colors
        self._current_puck: str = current_puck
        self._current_stage: str = current_stage
        self._gripper_state: int = gripper_state
        self._starting_zone_corner_order: List[str] = starting_zone_corner_order
        self._robot_position: dict = robot_position
        self._encoded_table_image: str = encoded_table_image
        self._battery_consumption: float = battery_consumption
