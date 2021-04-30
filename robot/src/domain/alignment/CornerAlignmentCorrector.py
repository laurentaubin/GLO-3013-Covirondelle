import numpy as np

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision.ICornerDetector import ICornerDetector


class CornerAlignmentCorrector:
    ALIGNMENT_SPEED = Speed(ROBOT_ALIGNMENT_SPEED)
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, ALIGNMENT_SPEED, CONTINUOUS_COMMAND_DURATION
    )
    RIGHT_MOVEMENT_COMMAND = MovementCommand(
        Direction.RIGHT, ALIGNMENT_SPEED, CONTINUOUS_COMMAND_DURATION
    )
    LEFT_MOVEMENT_COMMAND = MovementCommand(
        Direction.LEFT, ALIGNMENT_SPEED, CONTINUOUS_COMMAND_DURATION
    )
    FORWARD_MOVEMENT_COMMAND = MovementCommand(
        Direction.FORWARD, ALIGNMENT_SPEED, CONTINUOUS_COMMAND_DURATION
    )

    def __init__(
        self,
        corner_detector: ICornerDetector,
        corner_alignment_reference_position: Position,
    ):
        self._corner_detector = corner_detector
        self._corner_alignment_reference_position = corner_alignment_reference_position

    def calculate_horizontal_correction(self, image: np.ndarray) -> MovementCommand:
        corner_position: Position = self._corner_detector.detect_inferior_corner(image)
        horizontal_distance_from_reference_position = (
            corner_position.get_x_coordinate()
            - self._corner_alignment_reference_position.get_x_coordinate()
        )
        if horizontal_distance_from_reference_position == 0:
            return self.STOP_MOVEMENT_COMMAND
        return self._calculate_horizontal_movement_command(
            horizontal_distance_from_reference_position
        )

    def calculate_vertical_correction(self, image: np.ndarray) -> MovementCommand:
        corner_position: Position = self._corner_detector.detect_inferior_corner(image)
        corner_vertical_distance_from_reference_position = (
            corner_position.get_y_coordinate()
            - self._corner_alignment_reference_position.get_y_coordinate()
        )
        if corner_vertical_distance_from_reference_position < 0:
            return self.FORWARD_MOVEMENT_COMMAND
        return self.STOP_MOVEMENT_COMMAND

    def _calculate_horizontal_movement_command(
        self, horizontal_distance_from_reference_position: int
    ):
        if horizontal_distance_from_reference_position < 0:
            return self.LEFT_MOVEMENT_COMMAND
        return self.RIGHT_MOVEMENT_COMMAND
