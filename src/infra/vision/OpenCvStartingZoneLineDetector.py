from typing import List

import cv2
import numpy as np

from domain.Position import Position
from domain.Color import Color
from domain.vision.IStartingZoneLineDetector import IStartingZoneLineDetector
from domain.vision.exception.StartingZoneLineNotFoundException import (
    StartingZoneLineNotFoundException,
)


class OpenCvStartingZoneLineDetector(IStartingZoneLineDetector):
    def detect(self, image: np.ndarray) -> Position:
        image = self._cut_image(image)
        hsv_image = self._prepare_mask(image)
        contour = self._find_line_contour(hsv_image)
        moments = cv2.moments(contour)
        cx, cy = int(moments["m10"] / moments["m00"]), int(
            moments["m01"] / moments["m00"]
        )
        return Position(int(cx), int(cy))

    def _prepare_mask(self, image: np.ndarray):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_lower_bound, hsv_higher_bound = Color.STARTING_ZONE.get_hsv_bounds()
        return cv2.inRange(
            hsv_image, np.array(hsv_lower_bound), np.array(hsv_higher_bound)
        )

    def _find_line_contour(self, hsv_image: np.ndarray):
        contours, _ = cv2.findContours(
            hsv_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            raise StartingZoneLineNotFoundException()
        return self._extract_max_contour(contours)

    def _extract_max_contour(self, contours: List[np.ndarray]):
        return max(contours, key=cv2.contourArea)

    def _cut_image(self, image: np.ndarray) -> np.ndarray:
        return image[320:, :]
