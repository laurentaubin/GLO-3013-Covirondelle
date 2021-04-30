import numpy as np

from domain.Position import Position


class ICornerDetector:
    def detect_inferior_corner(self, image: np.ndarray) -> Position:
        pass
