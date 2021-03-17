from typing import List

from domain.Position import Position


class IObstacleDetector:
    def detect(self, image) -> List[Position]:
        pass
