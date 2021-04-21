import base64
from typing import List

import cv2
import numpy as np

from application.dto.GameStateDto import GameStateDto
from domain.Position import Position
from domain.Color import Color
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.game.GameState import GameState
from domain.game.Stage import Stage
from domain.pathfinding.Path import Path
from domain.resistance.Resistance import Resistance


class GameStateDtoAssembler:
    BOOT_STAGE_STRING = Stage.BOOT.value
    EMPTY_ARRAY: List = []
    GRIPPER_INITIAL_STATE: int = 0
    BASE_POSITION: Position = Position(0, 0)
    EMPTY_IMAGE: np.ndarray = np.ndarray([])
    NO_CONSUMPTION: float = 0.0
    NO_BATTERY_TIME_LEFT: float = 0.0
    NO_BATTERY_PERCENTAGE: float = 0.0
    NO_POWER_CONSUMPTION_FIRST_WHEEL: float = 0.0
    NO_POWER_CONSUMPTION_SECOND_WHEEL: float = 0.0
    NO_POWER_CONSUMPTION_THIRD_WHEEL: float = 0.0
    NO_POWER_CONSUMPTION_FOURTH_WHEEL: float = 0.0
    NO_RESISTANCE_VALUE: int = 0

    def assemble_from_game_state(self, game_state: GameState):
        puck_colors = self._get_puck_colors(game_state.get_puck_colors())
        current_puck = self._get_current_colors(game_state.get_current_puck())
        current_stage = self._get_current_stage(game_state.get_current_stage())
        gripper_state = self._get_gripper_state(game_state.get_gripper_state())
        starting_zone_corner_order = self._get_starting_zone_corner_order(
            game_state.get_starting_zone_corners()
        )
        robot_position = self._get_robot_position(game_state.get_robot_pose())
        battery_consumption = self._get_battery_consumption(
            game_state.get_battery_consumption()
        )
        is_game_started = game_state.is_game_cycle_started()
        current_planned_trajectory = self._get_current_planned_trajectory(
            game_state.get_current_planned_trajectory()
        )
        is_robot_booted = game_state.is_robot_booted()

        battery_time_left = self._get_power_consumption_first_wheel(
            game_state.get_battery_time_left()
        )
        battery_percentage = self._get_battery_time_left(
            game_state.get_battery_percentage()
        )
        power_consumption_first_wheel = self._get_power_consumption_first_wheel(
            game_state.get_power_consumption_first_wheel()
        )
        power_consumption_second_wheel = self._get_power_consumption_second_wheel(
            game_state.get_power_consumption_second_wheel()
        )
        power_consumption_third_wheel = self._get_power_consumption_third_wheel(
            game_state.get_power_consumption_third_wheel()
        )
        power_consumption_fourth_wheel = self._get_power_consumption_fourth_wheel(
            game_state.get_power_consumption_fourth_wheel()
        )
        resistance_value = self._get_resistance_value(game_state.get_resistance_value())
        return GameStateDto(
            puck_colors,
            current_puck,
            current_stage,
            gripper_state,
            starting_zone_corner_order,
            robot_position,
            battery_consumption,
            is_game_started,
            is_robot_booted,
            current_planned_trajectory,
            battery_time_left,
            battery_percentage,
            power_consumption_first_wheel,
            power_consumption_second_wheel,
            power_consumption_third_wheel,
            power_consumption_fourth_wheel,
            resistance_value,
        )

    def _get_puck_colors(self, puck_colors: List[Color]) -> List[str]:
        return (
            [puck_color.name for puck_color in puck_colors]
            if puck_colors is not None
            else self.EMPTY_ARRAY
        )

    def _get_current_colors(self, current_puck: Color) -> str:
        return current_puck.name if current_puck is not None else self.EMPTY_ARRAY

    def _get_current_stage(self, current_stage: Stage) -> str:
        return (
            current_stage.value if current_stage is not None else self.BOOT_STAGE_STRING
        )

    def _get_gripper_state(self, gripper_state: int) -> int:
        return (
            gripper_state if gripper_state is not None else self.GRIPPER_INITIAL_STATE
        )

    def _get_starting_zone_corner_order(
        self, starting_zone_corner_order: List[StartingZoneCorner]
    ) -> List[str]:
        return (
            [corner.name for corner in starting_zone_corner_order]
            if starting_zone_corner_order is not None
            else self.EMPTY_ARRAY
        )

    def _get_robot_position(self, robot_pose: RobotPose) -> dict:
        return (
            robot_pose.get_position().to_dictionary()
            if robot_pose is not None
            else self.BASE_POSITION.to_dictionary()
        )

    def _get_table_image(self, table_image: np.ndarray) -> np.ndarray:
        return table_image if table_image is not None else self.EMPTY_IMAGE

    def _get_battery_consumption(self, battery_consumption: float) -> float:
        return (
            battery_consumption
            if battery_consumption is not None
            else self.NO_CONSUMPTION
        )

    def _get_current_planned_trajectory(
        self, current_planned_trajectory: Path
    ) -> List[Position]:
        return (
            [position.to_dictionary() for position in current_planned_trajectory]
            if current_planned_trajectory is not None
            else self.EMPTY_ARRAY
        )

    def _get_battery_time_left(self, battery_time_left: float) -> float:
        return (
            battery_time_left
            if battery_time_left is not None
            else self.NO_BATTERY_TIME_LEFT
        )

    def _get_battery_percentage(self, battery_percentage: float) -> float:
        return (
            battery_percentage
            if battery_percentage is not None
            else self.NO_BATTERY_PERCENTAGE
        )

    def _get_power_consumption_first_wheel(
        self, power_consumption_first_wheel: float
    ) -> float:
        return (
            power_consumption_first_wheel
            if power_consumption_first_wheel is not None
            else self.NO_POWER_CONSUMPTION_FIRST_WHEEL
        )

    def _get_power_consumption_second_wheel(
        self, power_consumption_second_wheel: float
    ) -> float:
        return (
            power_consumption_second_wheel
            if power_consumption_second_wheel is not None
            else self.NO_POWER_CONSUMPTION_SECOND_WHEEL
        )

    def _get_power_consumption_third_wheel(
        self, power_consumption_third_wheel: float
    ) -> float:
        return (
            power_consumption_third_wheel
            if power_consumption_third_wheel is not None
            else self.NO_POWER_CONSUMPTION_THIRD_WHEEL
        )

    def _get_power_consumption_fourth_wheel(
        self, power_consumption_fourth_wheel: float
    ) -> float:
        return (
            power_consumption_fourth_wheel
            if power_consumption_fourth_wheel is not None
            else self.NO_POWER_CONSUMPTION_FIRST_WHEEL
        )

    def _get_resistance_value(self, resistance_value: Resistance) -> int:
        return (
            resistance_value.get_value()
            if resistance_value is not None
            else self.NO_RESISTANCE_VALUE
        )
