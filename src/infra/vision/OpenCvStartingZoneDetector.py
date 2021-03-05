import cv2
from typing import List

from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from infra.exception.StartingZoneCenterDetectedOutsideStartingZone import (
    StartingZoneCenterDetectedOutsideStartingZone,
)
from infra.exception.StartingZoneCenterNotFound import StartingZoneCenterNotFound
from infra.exception.StartingZoneCornersNotFound import StartingZoneCornersNotFound


class OpenCvStartingZoneDetector(IStartingZoneDetector):
    def detect(self, image) -> StartingZone:
        corners_list = self._detect_starting_zone_corners(image)
        starting_zone_center = self._detect_starting_zone_center(image)
        self._validate_center(corners_list, starting_zone_center)
        return StartingZone(corners_list, starting_zone_center)

    def _detect_starting_zone_corners(self, image) -> List[Position]:
        image_coordinate_y_axis = 700
        image_coordinate_x_axis = 800

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray_image, 4, 0.01, 50)

        corners_list = []
        for corner in corners:
            x, y = corner.ravel()

            if y < image_coordinate_y_axis and x < image_coordinate_x_axis:
                corners_list.append(Position(x, y))
        if len(corners_list) != 4:
            raise StartingZoneCornersNotFound
        return corners_list

    def _detect_starting_zone_center(self, image) -> Position:
        blurred_image = cv2.GaussianBlur(image, (7, 7), 1)
        gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
        canny_image = cv2.Canny(gray_image, 50, 190)
        contours, hierarchy = cv2.findContours(
            canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        for contour in contours:
            minimum_area = 9000
            area = cv2.contourArea(contour)
            if area > minimum_area:
                square_moment = cv2.moments(contour)
                x_coordinate = int(square_moment["m10"] / square_moment["m00"])
                y_coordinate = int(square_moment["m01"] / square_moment["m00"])

                return Position(x_coordinate, y_coordinate)

        raise StartingZoneCenterNotFound

    def _validate_center(self, corners_list, starting_zone_center):
        if (
            corners_list[2].get_x_coordinate()
            > starting_zone_center.get_x_coordinate()
            < corners_list[1].get_x_coordinate()
            and corners_list[2].get_y_coordinate()
            > starting_zone_center.get_y_coordinate()
            < corners_list[1].get_y_coordinate()
        ):
            raise StartingZoneCenterDetectedOutsideStartingZone
