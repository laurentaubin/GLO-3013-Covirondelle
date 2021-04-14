from typing import List

import cv2
import numpy as np

from domain.Color import Color
from domain.Position import Position
from domain.vision.IPuckDetector import IPuckDetector
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException


class OpenCvPuckDetector(IPuckDetector):
    def detect(self, image: np.ndarray, puck_color: Color) -> Position:
        cropped_image = self._cut_image(image)
        return self._new_find_puck(cropped_image, puck_color)

    def _new_find_puck(self, image: np.ndarray, puck_color: Color) -> Position:
        prepared_image = None
        if puck_color == Color.RED or puck_color == Color.BROWN:
            prepared_image = self._apply_two_mask(image, puck_color)
        elif (
            puck_color == Color.BLACK
            or puck_color == Color.GREY
            or puck_color == Color.WHITE
        ):
            prepared_image = self._prepared_image_to_find_with_just_circles(
                image, puck_color
            )

        else:
            prepared_image = self._new_prepared_image(image, puck_color)
        contour = self._new_find_puck_contour(prepared_image)
        (x, y), _ = cv2.minEnclosingCircle(contour)
        return Position(int(x), int(y))

    def _new_find_puck_contour(self, prepared_image: np.ndarray) -> np.ndarray:
        contours, *_ = cv2.findContours(
            prepared_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            raise PuckNotFoundException()
        good_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                print(cv2.contourArea(contour))
                good_contours.append(contour)
        if len(good_contours) == 0:
            raise PuckNotFoundException()
        return self._extract_max_contour(contours)

    def _prepared_image_to_find_with_just_circles(
        self, image: np.ndarray, color: Color
    ) -> np.ndarray:
        image_copy = image.copy()
        height, width, *_ = image_copy.shape
        mask = np.zeros((height, width), np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.GaussianBlur(image, (5, 5), 2)
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            1,
            12,
            param1=30,
            param2=30,
            minRadius=50,
            maxRadius=85,
        )
        for i in circles[0, :]:
            i[2] = i[2] - 5
            cv2.circle(
                mask,
                (int(i[0]), int(i[1])),
                int(i[2]),
                (255, 255, 255),
                thickness=-1,
            )
        masked_data = cv2.bitwise_and(image_copy, image_copy, mask=mask)
        return self._new_prepared_image(masked_data, color)

    def _new_prepared_image(self, image: np.ndarray, puck_color: Color) -> np.ndarray:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_bounds = puck_color.get_hsv_bounds()
        print(hsv_bounds)
        return cv2.inRange(
            hsv_image, np.array(hsv_bounds[0][0]), np.array(hsv_bounds[0][1])
        )

    def _apply_two_mask(self, image: np.ndarray, color: Color) -> np.ndarray:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_bounds = color.get_hsv_bounds()
        first_range = hsv_bounds[0][0]
        second_range = hsv_bounds[0][1]
        first_mask = cv2.inRange(
            hsv_image, np.array(first_range[0]), np.array(first_range[1])
        )
        second_mask = cv2.inRange(
            hsv_image, np.array(second_range[0]), np.array(second_range[1])
        )
        mask = first_mask + second_mask
        hsv_image[np.where(mask == 0)] = 0
        prepared_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return cv2.cvtColor(prepared_image, cv2.COLOR_BGR2GRAY)

    def _find_puck_contour(self, prepared_image: np.ndarray) -> np.ndarray:
        contours, *_ = cv2.findContours(
            prepared_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            raise PuckNotFoundException()
        return self._extract_max_contour(contours)

    def _extract_max_contour(self, contours: List[np.ndarray]):
        return max(contours, key=cv2.contourArea)

    def _cut_image(self, image: np.ndarray) -> np.ndarray:
        return image[:430, :]


# 14 avril: On peut  le laisser pour tester rapidement en cas de problème, le code ne fonctionne pas encore parfaitement
if __name__ == "__main__":
    # filename = "../../../resources/puck-color/image-{}.jpg"
    filename = "../../../resources/puck-color/image-7.jpg"
    files = []
    for i in range(1):
        files.append(filename.format(i))
    for image_filename in files:
        image = cv2.imread(image_filename)
        detector = OpenCvPuckDetector()
        try:
            position = detector.detect(image, Color.YELLOW)
            cv2.circle(
                image,
                (int(position.get_x_coordinate()), int(position.get_y_coordinate())),
                20,
                (0, 255, 0),
                2,
            )
            cv2.imshow("sda", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except PuckNotFoundException:
            cv2.imshow("sda", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("Puck not found")
