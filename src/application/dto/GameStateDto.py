from typing import List

from domain.Position import Position


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
        is_game_started: bool,
        current_planned_trajectory: List[Position],
    ):
        self._puck_colors: List[str] = puck_colors
        self._current_puck: str = current_puck
        self._current_stage: str = current_stage
        self._gripper_state: int = gripper_state
        self._starting_zone_corner_order: List[str] = starting_zone_corner_order
        self._robot_position: dict = robot_position
        self._encoded_table_image: str = encoded_table_image
        self._battery_consumption: float = battery_consumption
        self._is_game_started: bool = is_game_started
        self._current_planned_trajectory: List[Position] = current_planned_trajectory
