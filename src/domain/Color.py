from enum import Enum
from typing import Tuple, List


class Color(Enum):
    BLACK = 0, ([0, 0, 0], [179, 161, 22])
    BROWN = 1, ([0, 50, 0], [45, 255, 56])
    RED = 2, ([0, 0, 0], [10, 255, 255])
    ORANGE = 3, ([4, 103, 100], [15, 255, 255])
    YELLOW = 4, ([20, 129, 0], [35, 255, 255])
    GREEN = 5, ([48, 105, 39], [79, 255, 255])
    BLUE = 6, ([80, 0, 0], [120, 255, 255])
    PURPLE = 7, ([113, 8, 125], [179, 74, 196])
    GREY = 8, ([23, 0, 0], [80, 105, 107])
    WHITE = 9, ([0, 0, 157], [179, 47, 195])
    NONE = 10, ([0, 0, 0], [0, 0, 0])

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
