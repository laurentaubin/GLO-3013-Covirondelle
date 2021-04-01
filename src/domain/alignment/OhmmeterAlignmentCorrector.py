import numpy as np

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision.IStartingZoneLineDetector import IStartingZoneLineDetector


class OhmmeterAlignmentCorrector:
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CommandDuration(0)
    )

    def __init__(
        self,
        aligned_ohmmeter_position: Position,
        horizontal_threshold: int,
        starting_zone_line_detector: IStartingZoneLineDetector,
    ):
        self._aligned_ohmmeter_position: Position = aligned_ohmmeter_position
        self._horizontal_threshold: int = horizontal_threshold
        self._starting_zone_line_detector: IStartingZoneLineDetector = (
            starting_zone_line_detector
        )

    def calculate_horizontal_correction(self, image: np.ndarray) -> MovementCommand:
        starting_zone_line_position: Position = (
            self._starting_zone_line_detector.detect(image)
        )
        horizontal_distance_from_being_aligned = (
            self._aligned_ohmmeter_position.get_x_coordinate()
            - starting_zone_line_position.get_x_coordinate()
        )

        if abs(horizontal_distance_from_being_aligned) <= self._horizontal_threshold:
            return self.STOP_MOVEMENT_COMMAND

        if self._is_line_to_the_right(horizontal_distance_from_being_aligned):
            return MovementCommand(
                Direction.RIGHT, ROBOT_ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
            )
        return MovementCommand(
            Direction.LEFT, ROBOT_ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
        )

    def _is_line_to_the_right(
        self, horizontal_distance_from_being_aligned: int
    ) -> bool:
        return horizontal_distance_from_being_aligned < 0
