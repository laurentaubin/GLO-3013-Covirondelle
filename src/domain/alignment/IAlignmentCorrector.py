import numpy as np

from domain.movement.Movement import Movement
from domain.resistance.ResistanceColor import ResistanceColor


class IAlignmentCorrector:
    def calculate_horizontal_correction(
        self, image: np.ndarray, puck_color: ResistanceColor
    ) -> Movement:
        pass

    def calculate_vertical_correction(
        self, image: np.ndarray, puck_color: ResistanceColor
    ) -> Movement:
        pass
