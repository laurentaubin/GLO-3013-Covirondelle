import numpy as np

from domain.movement.MovementCommand import MovementCommand
from domain.vision.Color import Color


class IAlignmentCorrector:
    def calculate_horizontal_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        pass

    def calculate_vertical_correction(
        self, image: np.ndarray, puck_color: Color
    ) -> MovementCommand:
        pass
