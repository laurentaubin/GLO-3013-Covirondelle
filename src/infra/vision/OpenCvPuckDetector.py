import numpy as np
import cv2
from domain.Position import Position
from domain.Color import Color
from domain.vision.IPuckDetector import IPuckDetector
from infra.exception import PuckCenterNotFound
from infra.utils.VisionUtils import VisionUtils

X_VALUE = 1200
MINIMUM_AREA = 800


class OpenCvPuckDetector(IPuckDetector):
    def detect(self, image: np.array, color: Color) -> Position:
        mask = self._prepare_mask(image, color)
        contours, hierarchy = cv2.findContours(
            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )

        for bound, contour in enumerate(contours):

            if hierarchy[0][bound][3] == -1:
                contours_polygon = cv2.approxPolyDP(contour, 3, True)
                bounding_rectangle = cv2.boundingRect(contours_polygon)

                rectangle_x = bounding_rectangle[0]
                rectangle_y = bounding_rectangle[1]
                rectangle_width = bounding_rectangle[2]
                rectangle_height = bounding_rectangle[3]

                rectangle_area = rectangle_width * rectangle_height
                aspect_ratio = rectangle_width / rectangle_height
                delta = abs(1.0 - aspect_ratio)
                epsilon = 0.2
                if (
                    rectangle_area > MINIMUM_AREA
                    and delta < epsilon
                    and rectangle_x > X_VALUE
                ):

                    puck_center = Position(
                        int(rectangle_x + rectangle_width / 2),
                        int(rectangle_y + rectangle_height / 2),
                    )
                    return puck_center
        raise PuckCenterNotFound

    def _prepare_mask(self, image, color):
        frame_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_bounds = color.get_hsv_bounds()
        lower_hsv = np.array(hsv_bounds[0])
        upper_hsv = np.array(hsv_bounds[1])
        mask = cv2.inRange(frame_hsv, lower_hsv, upper_hsv)
        mask = VisionUtils.apply_area_filter(MINIMUM_AREA, mask)
        kernel_size = 3

        structuring_element = cv2.getStructuringElement(
            cv2.MORPH_RECT, (kernel_size, kernel_size)
        )

        iterations = 10
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_DILATE,
            structuring_element,
            None,
            None,
            iterations,
            cv2.BORDER_REFLECT101,
        )
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_ERODE,
            structuring_element,
            None,
            None,
            iterations,
            cv2.BORDER_REFLECT101,
        )
        return mask
