from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.vision.ICornerDetector import ICornerDetector

import cv2


class OpenCvCornerDetector(ICornerDetector):
    def detect_starting_zone(self, image) -> {"StartingZone"}:

        image_coordinate_y_axis = 700
        image_coordinate_x_axis = 800

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_image, 4, 0.01, 50)

        corners_list = []
        for corner in corners:
            x, y = corner.ravel()

            if y < image_coordinate_y_axis and x < image_coordinate_x_axis:
                corners_list.append(Position(x, y))

        return StartingZone(corners_list)
