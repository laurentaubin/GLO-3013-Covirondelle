import numpy as np

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.alignment.IAlignmentCorrector import IAlignmentCorrector
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision import IPuckDetector
from domain.vision.Color import Color


class PuckAlignmentCorrector(IAlignmentCorrector):
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CONTINUOUS_COMMAND_DURATION
    )

    def __init__(
        self,
        image_central_point: Position,
        center_position_threshold: int,
        puck_detector: IPuckDetector,
    ):
        self._image_central_point = image_central_point
        self._center_position_threshold = center_position_threshold
        self._puck_detector = puck_detector

    def calculate_horizontal_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        puck_position: Position = self._puck_detector.detect(image, puck_color)
        horizontal_distance_from_center: int = (
            puck_position.get_x_coordinate()
            - self._image_central_point.get_x_coordinate()
        )
        if self._is_puck_position_within_horizontal_threshold(
            horizontal_distance_from_center
        ):
            return self.STOP_MOVEMENT_COMMAND
        return self._calculate_horizontal_movement_command(
            horizontal_distance_from_center
        )

    def calculate_vertical_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        puck_position: Position = self._puck_detector.detect(image, puck_color)

        vertical_distance_from_center: int = (
            puck_position.get_y_coordinate()
            - self._image_central_point.get_y_coordinate()
        )
        if self._is_puck_within_vertical_threshold(vertical_distance_from_center):
            return self.STOP_MOVEMENT_COMMAND
        return self._calculate_vertical_movement_command(vertical_distance_from_center)

    def _is_puck_position_within_horizontal_threshold(
        self, horizontal_distance_from_center: int
    ) -> bool:
        return abs(horizontal_distance_from_center) <= self._center_position_threshold

    def _calculate_horizontal_movement_command(
        self, distance_from_center: int
    ) -> MovementCommand:
        if self._is_puck_to_the_left(distance_from_center):
            return MovementCommand(
                Direction.LEFT,
                Speed(ROBOT_ALIGNMENT_SPEED),
                self.CONTINUOUS_COMMAND_DURATION,
            )
        return MovementCommand(
            Direction.RIGHT,
            Speed(ROBOT_ALIGNMENT_SPEED),
            self.CONTINUOUS_COMMAND_DURATION,
        )

    def _is_puck_to_the_left(self, distance_from_center: int) -> bool:
        return distance_from_center < 0

    def _calculate_vertical_movement_command(
        self, vertical_distance_from_center: int
    ) -> MovementCommand:
        if self._is_puck_too_close(vertical_distance_from_center):
            return MovementCommand(
                Direction.BACKWARDS,
                Speed(ROBOT_ALIGNMENT_SPEED),
                self.CONTINUOUS_COMMAND_DURATION,
            )
        return MovementCommand(
            Direction.FORWARD,
            Speed(ROBOT_ALIGNMENT_SPEED),
            self.CONTINUOUS_COMMAND_DURATION,
        )

    def _is_puck_too_close(self, vertical_distance_from_center: int) -> bool:
        return vertical_distance_from_center > 0

    def _is_puck_within_vertical_threshold(
        self, vertical_distance_from_center: int
    ) -> bool:
        return abs(vertical_distance_from_center) <= self._center_position_threshold
