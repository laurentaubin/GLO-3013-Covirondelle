import cv2
import numpy as np

from config.config import IMAGE_CENTER_POSITION
from domain.Position import Position
from domain.vision.ICornerDetector import ICornerDetector


class OpenCvCornerDetector(ICornerDetector):
    NUMBER_OF_CORNERS_TO_FIND = 3
    QUALITY_LEVEL = 0.01
    MIN_DISTANCE_BETWEEN_CORNERS = 10
    BLUR_KERNEL = (3, 3)
    NUMBER_OF_ITERATIONS = 1
    IMAGE_HEIGHT_TO_CUT_GRIPPER_FROM_VIEW = 320
    INFINITE_VALUE = float("inf")

    def detect_inferior_corner(self, image: np.ndarray) -> Position:
        prepared_image = self._prepare_image(image)
        corners = cv2.goodFeaturesToTrack(
            prepared_image,
            self.NUMBER_OF_CORNERS_TO_FIND,
            self.QUALITY_LEVEL,
            self.MIN_DISTANCE_BETWEEN_CORNERS,
        )
        good_corner = self._keep_good_corner(corners)
        x, y = good_corner.ravel()
        return Position(int(x), int(y))

    def _keep_good_corner(self, corners):
        min_delta_x = self.INFINITE_VALUE
        min_delta_y = self.INFINITE_VALUE
        good_corner = None

        for corner in corners:
            x, y = corner.ravel()
            if (
                abs(x - IMAGE_CENTER_POSITION[0]) < min_delta_x
                and abs(y - IMAGE_CENTER_POSITION[1]) < min_delta_y
            ):
                min_delta_x = abs(x - IMAGE_CENTER_POSITION[0])
                min_delta_y = abs(y - IMAGE_CENTER_POSITION[1])
                good_corner = corner
        return good_corner

    def _cut_gripper_from_image(self, image: np.ndarray) -> np.ndarray:
        return image[: self.IMAGE_HEIGHT_TO_CUT_GRIPPER_FROM_VIEW, :]

    def _prepare_image(self, image: np.ndarray) -> np.ndarray:
        image = self._cut_gripper_from_image(image.copy())
        image = cv2.GaussianBlur(image, self.BLUR_KERNEL, self.NUMBER_OF_ITERATIONS)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
