from typing import List

import cv2
import numpy as np

from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from infra.exception.StartingZoneCenterDetectedOutsideStartingZone import (
    StartingZoneCenterDetectedOutsideStartingZone,
)
from infra.exception.StartingZoneCornersNotFound import StartingZoneCornersNotFound
from infra.utils.VisionUtils import VisionUtils

AREA_MIN = 2500


class OpenCvStartingZoneDetector(IStartingZoneDetector):
    def detect(self, image) -> StartingZone:
        corners_list = self._find_starting_zone_corners(image)
        upper_left_corner = corners_list[0]
        bottom_right_corner = corners_list[3]
        center_x_coordinate = int(
            upper_left_corner.get_x_coordinate()
            + bottom_right_corner.get_x_coordinate() / 2
        )
        center_y_coordinate = int(
            upper_left_corner.get_y_coordinate()
            + bottom_right_corner.get_y_coordinate() / 2
        )
        starting_zone_center = Position(center_x_coordinate, center_y_coordinate)
        self._validate_center(corners_list, starting_zone_center)
        return StartingZone(corners_list, starting_zone_center)

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

    def _find_starting_zone_corners(self, image) -> List[Position]:
        mask = self._prepare_mask(image)
        contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        corners_list = []
        for contour in contours:
            contours_poly = cv2.approxPolyDP(contour, 3, True)
            bounding_rect = cv2.boundingRect(contours_poly)
            rect_X = bounding_rect[0]
            rect_y = bounding_rect[1]
            rect_width = bounding_rect[2]
            rect_height = bounding_rect[3]
            rectangle_area = rect_width * rect_height
            aspect_ratio = rect_width / rect_height
            delta = abs(1.0 - aspect_ratio)
            epsilon = 0.2
            if rectangle_area > AREA_MIN and delta < epsilon:
                top_left_corner = Position(rect_X, rect_y)
                corners_list.append(top_left_corner)
                top_right_corner = Position(rect_X + rect_width, rect_y)
                corners_list.append(top_right_corner)
                bottom_left_corner = Position(rect_X, rect_y + rect_height)
                corners_list.append(bottom_left_corner)
                bottom_right_corner = Position(
                    rect_X + rect_width, rect_y + rect_height
                )
                corners_list.append(bottom_right_corner)
        if len(corners_list) != 4:
            raise StartingZoneCornersNotFound
        return corners_list

    def _prepare_mask(self, image):
        lower_values = np.array([58, 151, 25])
        upper_values = np.array([86, 255, 75])
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, lower_values, upper_values)
        minimum_area = 50
        mask = VisionUtils.apply_area_filter(minimum_area, mask)
        kernel = 3
        structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel, kernel))
        iterations = 2
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_DILATE,
            structuringElement,
            None,
            None,
            iterations,
            cv2.BORDER_REFLECT101,
        )
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_ERODE,
            structuringElement,
            None,
            None,
            iterations,
            cv2.BORDER_REFLECT101,
        )
        return mask
