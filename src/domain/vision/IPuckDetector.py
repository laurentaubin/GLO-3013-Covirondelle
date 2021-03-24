import numpy as np

from domain.Position import Position
from domain.vision.Color import Color


class IPuckDetector:
    def detect(self, image: np.ndarray, puck_color: Color) -> Position:
        pass
