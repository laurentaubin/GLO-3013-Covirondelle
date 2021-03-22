import numpy as np

from domain.Position import Position
from domain.resistance.ResistanceColor import ResistanceColor


class IPuckDetector:
    def detect(self, image: np.ndarray, puck_color: ResistanceColor) -> Position:
        pass
