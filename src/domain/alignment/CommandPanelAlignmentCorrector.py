import time
from typing import List

import numpy as np

from domain.Position import Position
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
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
    ) -> Movement:
        time.sleep(1)
        command_panel_letters = (
            self._command_panel_letter_extractor.extract_letters_from_image(image)
        )
        if self._can_read_all_letters(command_panel_letters):
            return Movement(Direction.STOP, Distance(0))
        else:
            return Movement(Direction.RIGHT, Distance(0.1))

    def _can_read_all_letters(self, extracted_letters: List[str]) -> bool:
        return len(extracted_letters) == self._number_of_command_panel_letters
