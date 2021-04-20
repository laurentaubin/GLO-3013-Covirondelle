import cv2
import numpy as np

from domain.Color import Color
from domain.Position import Position
from domain.vision.IPuckDetector import IPuckDetector

PUCK_RADIUS_X = 76
PUCK_RADIUS_Y = 72


class TemplateMatchingPuckDetector(IPuckDetector):
    def detect(self, image: np.array, color: Color) -> Position:
        # image = self._cut_image(image)
        template = cv2.imread(color.get_template())
        res = cv2.matchTemplate(image, template, method=cv2.TM_CCORR_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        return Position(
            top_left[0] + PUCK_RADIUS_X,
            top_left[1] + PUCK_RADIUS_Y,
        )

    #
    # def _cut_image(self, image: np.ndarray) -> np.ndarray:
    #     return image[
    #         self.VERTICAL_CROP[0] : self.VERTICAL_CROP[1],
    #         self.HORIZONTAL_CROP[0] : self.HORIZONTAL_CROP[1],
    #     ]
