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


class GameStateDtoAssembler:
    BOOT_STAGE_STRING = Stage.BOOT.value
    EMPTY_ARRAY: List = []
    GRIPPER_INITIAL_STATE: int = 0
    BASE_POSITION: Position = Position(0, 0)
    EMPTY_IMAGE: np.ndarray = np.ndarray([])
    NO_CONSUMPTION: float = 0.0

    def assemble_from_game_state(self, game_state: GameState):
        puck_colors = self._get_puck_colors(game_state.get_puck_colors())
        current_puck = self._get_current_colors(game_state.get_current_puck())
        current_stage = self._get_current_stage(game_state.get_current_stage())
        gripper_state = self._get_gripper_state(game_state.get_prehensor_state())
        starting_zone_corner_order = self._get_starting_zone_corner_order(
            game_state.get_starting_zone_corners()
        )
        robot_position = self._get_robot_position(game_state.get_robot_pose())
        table_image = self._get_table_image(game_state.get_table_image())
        battery_consumption = self._get_battery_consumption(
            game_state.get_battery_consumption()
        )

        return GameStateDto(
            puck_colors,
            current_puck,
            current_stage,
            gripper_state,
            starting_zone_corner_order,
            robot_position,
            self._encode_image(table_image),
            battery_consumption,
        )

    def _get_puck_colors(self, puck_colors: List[Color]) -> List[str]:
        return (
            [puck_color.value for puck_color in puck_colors]
            if puck_colors is not None
            else self.EMPTY_ARRAY
        )

    def _get_current_colors(self, current_puck: Color) -> str:
        return current_puck.value if current_puck is not None else self.EMPTY_ARRAY

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
            [corner.value for corner in starting_zone_corner_order]
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

    def _encode_image(self, image: np.ndarray):
        _, buffer_img = cv2.imencode(".jpg", image)
        return base64.b64encode(buffer_img).decode()
