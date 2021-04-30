import cv2
import numpy as np

from domain.Position import Position
from domain.vision.ICommandPanelDetector import ICommandPanelDetector


class OpenCvCommandPanelDetector(ICommandPanelDetector):
    def detect_upper_left_corner(self, image: np.ndarray) -> Position:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        command_panel_contour = max(contours, key=cv2.contourArea)
        x, y, _, _ = cv2.boundingRect(command_panel_contour)

        return Position(x, y)
