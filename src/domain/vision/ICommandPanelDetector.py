import numpy as np

from domain.movement.MovementCommand import MovementCommand


class ICommandPanelDetector:
    def detect_upper_left_corner(self, image: np.ndarray) -> MovementCommand:
        pass
