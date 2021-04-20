import numpy as np

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Color import Color
from domain.Position import Position
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision import IPuckDetector
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException


class PuckAlignmentCorrector:
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CONTINUOUS_COMMAND_DURATION
    )

    def __init__(
        self,
        correctly_placed_position: Position,
        horizontal_threshold: int,
        up_threshold: int,
        horizontal_puck_detector: IPuckDetector,
        vertical_puck_detector: IPuckDetector,
    ):
        self.correctly_placed_position = correctly_placed_position
        self._horizontal_threshold = horizontal_threshold
        self._up_threshold = up_threshold
        self._horizontal_puck_detector = horizontal_puck_detector
        self._vertical_puck_detector = vertical_puck_detector

    def calculate_horizontal_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        try:
            puck_position: Position = self._horizontal_puck_detector.detect(
                image, puck_color
            )
            horizontal_distance_from_center: int = (
                puck_position.get_x_coordinate()
                - self.correctly_placed_position.get_x_coordinate()
            )
            if self._is_puck_position_within_horizontal_threshold(
                horizontal_distance_from_center
            ):
                return self.STOP_MOVEMENT_COMMAND
            return self._calculate_horizontal_movement_command(
                horizontal_distance_from_center
            )
        except PuckNotFoundException:
            return MovementCommand(
                Direction.FORWARD,
                Speed(ROBOT_ALIGNMENT_SPEED),
                self.CONTINUOUS_COMMAND_DURATION,
            )

    def calculate_vertical_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        puck_position: Position = self._vertical_puck_detector.detect(image, puck_color)

        if (
            puck_position.get_y_coordinate()
            >= self.correctly_placed_position.get_y_coordinate()
        ):
            return self.STOP_MOVEMENT_COMMAND

        return MovementCommand(
            Direction.FORWARD,
            Speed(ROBOT_ALIGNMENT_SPEED),
            self.CONTINUOUS_COMMAND_DURATION,
        )

    def _is_puck_position_within_horizontal_threshold(
        self, horizontal_distance_from_center: int
    ) -> bool:
        return abs(horizontal_distance_from_center) <= self._horizontal_threshold

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
