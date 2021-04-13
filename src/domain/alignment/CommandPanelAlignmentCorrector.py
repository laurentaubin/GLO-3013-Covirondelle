from typing import List

import numpy as np

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision import ICommandPanelDetector
from domain.vision import ILetterPositionExtractor


class CommandPanelAlignmentCorrector:
    def __init__(
        self,
        number_of_command_panel_letters: int,
        command_panel_reference_position: Position,
        panel_detector: ICommandPanelDetector,
        command_panel_letter_extractor: ILetterPositionExtractor,
    ):
        self._number_of_command_panel_letters = number_of_command_panel_letters
        self._command_panel_reference_position = command_panel_reference_position
        self._panel_detector = panel_detector
        self._command_panel_letter_extractor = command_panel_letter_extractor

    def calculate_horizontal_correction(
        self,
        image: np.ndarray,
    ) -> MovementCommand:
        command_panel_letters = (
            self._command_panel_letter_extractor.extract_letters_from_image(image)
        )

        if self._can_read_all_letters(command_panel_letters):
            return MovementCommand(Direction.STOP, Speed(0), CommandDuration(0))
        else:
            command_panel_upper_left_corner_position: Position = (
                self._panel_detector.detect_upper_left_corner(image)
            )
            if (
                command_panel_upper_left_corner_position.get_x_coordinate()
                < self._command_panel_reference_position.get_x_coordinate()
            ):
                return MovementCommand(
                    Direction.LEFT, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
                )
            else:
                return MovementCommand(
                    Direction.RIGHT, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
                )

    def _can_read_all_letters(self, extracted_letters: List[str]) -> bool:
        return len(extracted_letters) == self._number_of_command_panel_letters
