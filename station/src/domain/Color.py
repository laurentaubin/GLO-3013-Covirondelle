from enum import Enum
from typing import Tuple, List

from config.config import PUCK_TEMPLATE_LOCATION


class Color(Enum):
    BLACK = 0, ([0, 0, 0], [50, 161, 22]), PUCK_TEMPLATE_LOCATION + "black.jpg"
    BROWN = 1, ([9, 68, 0], [19, 255, 70]), PUCK_TEMPLATE_LOCATION + "brown.jpg"
    RED = 2, ([175, 173, 0], [179, 255, 255]), PUCK_TEMPLATE_LOCATION + "red.jpg"
    ORANGE = 3, ([5, 103, 100], [11, 255, 255]), PUCK_TEMPLATE_LOCATION + "orange.jpg"
    YELLOW = (
        4,
        ([22, 213, 121], [26, 255, 255]),
        PUCK_TEMPLATE_LOCATION + "yellow.jpg",
    )
    GREEN = 5, ([48, 105, 39], [79, 255, 255]), PUCK_TEMPLATE_LOCATION + "green.jpg"
    BLUE = 6, ([107, 139, 0], [119, 255, 255]), PUCK_TEMPLATE_LOCATION + "blue.jpg"
    PURPLE = 7, ([113, 8, 125], [179, 74, 196]), PUCK_TEMPLATE_LOCATION + "purple.jpg"
    GREY = 8, ([23, 0, 0], [80, 105, 107]), PUCK_TEMPLATE_LOCATION + "grey.jpg"
    WHITE = 9, ([0, 0, 157], [179, 47, 195]), PUCK_TEMPLATE_LOCATION + "white.jpg"
    NONE = 10, ([0, 0, 0], [0, 0, 0]), ""

    def __init__(
        self,
        resistance_digit: int,
        hsv_bounds: Tuple[List[int], List[int]],
        template: str,
    ):
        self._resistance_digit = resistance_digit
        self._hsv_bounds = hsv_bounds
        self._template = template

    def get_resistance_digit(self) -> int:
        return self._resistance_digit

    def get_hsv_bounds(self) -> Tuple[List[int], List[int]]:
        return self._hsv_bounds

    def get_template(self) -> str:
        return self._template

    @staticmethod
    def value_of_resistance_digit(digit: int) -> "Color":
        for color in Color:
            if digit == color.get_resistance_digit():
                return color
