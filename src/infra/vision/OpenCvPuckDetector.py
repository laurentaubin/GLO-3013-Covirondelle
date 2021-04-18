import numpy as np
import cv2
from domain.Position import Position
from domain.Color import Color
from domain.vision.IPuckDetector import IPuckDetector


class OpenCvPuckDetector(IPuckDetector):
    HORIZONTAL_CROP = (390, 612)
    VERTICAL_CROP = (112, 368)

    def detect(self, image: np.array, color: Color) -> Position:
        image = self._cut_image(image)
        image_result = self._prepare_image(image, color)
        puck_contour = self._find_contour(image_result)
        if len(puck_contour) == 0:
            return Position(0, 0)
        center, _ = cv2.minEnclosingCircle(puck_contour)
        return Position(
            int(center[0]) + self.HORIZONTAL_CROP[0],
            int(center[1]) + self.VERTICAL_CROP[0],
        )

    def _cut_image(self, image: np.ndarray) -> np.ndarray:
        return image[
            self.VERTICAL_CROP[0] : self.VERTICAL_CROP[1],
            self.HORIZONTAL_CROP[0] : self.HORIZONTAL_CROP[1],
        ]

    # https://www.javaer101.com/en/article/14982276.html
    def _prepare_image(self, image: np.ndarray, color: Color) -> np.ndarray:
        image_copy = image.copy()
        height, width, *_ = image.shape
        mask = np.zeros((height, width), np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.GaussianBlur(gray, (5, 5), 0)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            1,
            15,
            param1=30,
            param2=20,
            minRadius=8,
            maxRadius=16,
        )
        for i in circles[0, :]:
            i[2] = i[2] - 1
            cv2.circle(
                mask, (int(i[0]), int(i[1])), int(i[2]), (255, 255, 255), thickness=-1
            )
        masked_data = cv2.bitwise_and(image_copy, image_copy, mask=mask)
        lower, upper = color.get_hsv_bounds()
        return self._apply_hsv_bounds(np.array(lower), np.array(upper), masked_data)

    def _apply_hsv_bounds(self, lower, upper, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)
        return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    def _find_contour(self, image: np.ndarray) -> np.ndarray:
        contours, _hierarchy = cv2.findContours(
            image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            return np.array([])
        return max(contours, key=cv2.contourArea)
