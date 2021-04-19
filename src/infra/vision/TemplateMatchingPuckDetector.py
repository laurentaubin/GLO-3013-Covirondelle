import cv2
import numpy as np

from domain.Color import Color
from domain.Position import Position
from domain.vision.IPuckDetector import IPuckDetector


class TemplateMatchingPuckDetector(IPuckDetector):
    PUCK_RADIUS = 22
    HORIZONTAL_CROP = (780, 1250)
    VERTICAL_CROP = (120, 700)

    def detect(self, image: np.array, color: Color) -> Position:
        image = self._cut_image(image)
        template = cv2.imread(color.get_template())
        res = cv2.matchTemplate(image, template, method=cv2.TM_CCORR_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        return Position(
            top_left[0] + self.PUCK_RADIUS + self.HORIZONTAL_CROP[0],
            top_left[1] + self.PUCK_RADIUS + self.VERTICAL_CROP[0],
        )

    def _cut_image(self, image: np.ndarray) -> np.ndarray:
        return image[
            self.VERTICAL_CROP[0] : self.VERTICAL_CROP[1],
            self.HORIZONTAL_CROP[0] : self.HORIZONTAL_CROP[1],
        ]
