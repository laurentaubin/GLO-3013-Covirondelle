from enum import Enum


class Color(Enum):
    BLACK = 0, ([70, 0, 0], [133, 255, 57])
    BROWN = 1, (([4, 68, 0], [18, 255, 72]), ([8, 25, 17], [18, 185, 143]))
    RED = 2, (([0, 70, 0], [2, 255, 255]), ([170, 70, 50], [189, 255, 255]))
    ORANGE = 3, ([5, 120, 120], [19, 255, 255])
    YELLOW = 4, ([19, 171, 0], [31, 255, 255])
    GREEN = 5, ([48, 105, 39], [79, 255, 255])
    BLUE = 6, ([103, 0, 83], [126, 255, 255])
    PURPLE = 7, ([114, 0, 10], [158, 109, 255])
    GREY = 8, ([20, 4, 0], [47, 141, 133])
    WHITE = 9, ([0, 0, 157], [172, 111, 255])
    NONE = 10, ([0, 0, 0], [0, 0, 0])
    STARTING_ZONE = 11, ([30, 0, 0], [80, 240, 114])
    INTERIOR_BLUE = 12, ([77, 0, 124], [94, 255, 255])

    def __init__(self, resistance_digit: int, *hsv_bounds):
        self._resistance_digit = resistance_digit
        self._hsv_bounds = hsv_bounds

    def get_resistance_digit(self) -> int:
        return self._resistance_digit

    def get_hsv_bounds(self):
        return self._hsv_bounds

    @staticmethod
    def value_of_resistance_digit(digit: int) -> "Color":
        for color in Color:
            if digit == color.get_resistance_digit():
                return color
