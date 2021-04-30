import numpy as np

from domain.Color import Color
from domain.Position import Position


class IPuckDetector:
    def detect(self, image: np.array, color: Color) -> Position:
        pass
