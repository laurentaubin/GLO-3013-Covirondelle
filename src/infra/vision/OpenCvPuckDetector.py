from typing import List

import cv2
import numpy as np

from domain.Position import Position
from domain.vision.Color import Color
from domain.vision.IPuckDetector import IPuckDetector
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException


class OpenCvPuckDetector(IPuckDetector):
    def detect(self, image: np.ndarray, puck_color: Color) -> Position:
        hsv_image = self._prepare_mask(image, puck_color)
        contour = self._find_puck_contour(hsv_image)
        (x, y), _ = cv2.minEnclosingCircle(contour)
        return Position(int(x), int(y))

    def _prepare_mask(self, image: np.ndarray, puck_color: Color):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_lower_bound, hsv_higher_bound = puck_color.get_hsv_bounds()
        return cv2.inRange(
            hsv_image, np.array(hsv_lower_bound), np.array(hsv_higher_bound)
        )

    def _find_puck_contour(self, hsv_image: np.ndarray) -> np.ndarray:
        contours, _ = cv2.findContours(
            hsv_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            raise PuckNotFoundException()
        return self._extract_max_contour(contours)

    def _extract_max_contour(self, contours: List[np.ndarray]):
        return max(contours, key=cv2.contourArea)
