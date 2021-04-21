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
        battery_consumption: float,
        is_game_started: bool,
        is_robot_booted: bool,
        current_planned_trajectory: List[Position],
        battery_time_left: float,
        battery_percentage: float,
        power_consumption_first_wheel: float,
        power_consumption_second_wheel: float,
        power_consumption_third_wheel: float,
        power_consumption_fourth_wheel: float,
        resistance_value: int,
    ):
        self._puck_colors: List[str] = puck_colors
        self._current_puck: str = current_puck
        self._current_stage: str = current_stage
        self._gripper_state: int = gripper_state
        self._starting_zone_corner_order: List[str] = starting_zone_corner_order
        self._robot_position: dict = robot_position
        self._battery_consumption: float = battery_consumption
        self._is_game_started: bool = is_game_started
        self._is_robot_booted: bool = is_robot_booted
        self._current_planned_trajectory: List[Position] = current_planned_trajectory
        self._battery_time_left = battery_time_left
        self._battery_percentage = battery_percentage
        self._power_consumption_first_wheel = power_consumption_first_wheel
        self._power_consumption_second_wheel = power_consumption_second_wheel
        self._power_consumption_third_wheel = power_consumption_third_wheel
        self._power_consumption_fourth_wheel = power_consumption_fourth_wheel
        self._resistance_value = resistance_value

    def __repr__(self):
        return f"{self._robot_position}"
