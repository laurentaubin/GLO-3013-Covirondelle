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
        (x, y), _ = cv2.minEnclosingCircle(contour)
        return Position(int(x), int(y) + 320)

    def _prepare_mask(self, image: np.ndarray):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_bounds = Color.STARTING_ZONE.get_hsv_bounds()
        return cv2.inRange(
            hsv_image, np.array(hsv_bounds[0][0]), np.array(hsv_bounds[0][1])
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


if __name__ == "__main__":
    detector = OpenCvStartingZoneLineDetector()
    image = cv2.imread("../../../resources/aligment-good-angle/station-aligned.jpeg")

    position = detector.detect(image)
    print(position.to_tuple())
    cv2.circle(image, position.to_tuple(), 20, (0, 255, 0), 2)
    cv2.imshow("ima", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
