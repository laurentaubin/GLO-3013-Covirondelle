import numpy as np

from domain.movement.MovementCommand import MovementCommand


class ICommandPanelDetector:
    def detect(self, image: np.ndarray) -> MovementCommand:
        pass
