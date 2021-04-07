from enum import Enum
from typing import Tuple, List


class Color(Enum):
    BLACK = 0, ([0, 0, 0], [179, 255, 21])
    BROWN = 1, ([6, 63, 0], [23, 255, 81])
    RED = 2, ([0, 123, 40], [5, 255, 114])
    ORANGE = 3, ([4, 103, 100], [15, 255, 255])
    YELLOW = 4, ([20, 100, 100], [30, 255, 255])
    GREEN = 5, ([48, 105, 39], [79, 255, 255])
    BLUE = 6, ([80, 160, 20], [120, 255, 255])
    PURPLE = 7, ([119, 37, 95], [176, 84, 138])
    GREY = 8, ([23, 0, 0], [80, 105, 107])
    WHITE = 9, ([37, 0, 131], [170, 25, 152])
    NONE = 10, ([0, 0, 0], [0, 0, 0])
    STARTING_ZONE = 11, ([58, 110, 5], [86, 255, 255])

    def __init__(self, resistance_digit: int, hsv_bounds: Tuple[List[int], List[int]]):
        self._resistance_digit = resistance_digit
        self._hsv_bounds = hsv_bounds

    def get_resistance_digit(self) -> int:
        return self._resistance_digit

    def get_hsv_bounds(self) -> Tuple[List[int], List[int]]:
        return self._hsv_bounds

    @staticmethod
    def value_of_resistance_digit(digit: int) -> "Color":
        for color in Color:
            if digit == color.get_resistance_digit():
                return color
