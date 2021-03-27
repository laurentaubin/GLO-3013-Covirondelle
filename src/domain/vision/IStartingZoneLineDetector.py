import numpy as np

from domain.Position import Position


class IStartingZoneLineDetector:
    def detect(self, image: np.ndarray) -> Position:
        pass
