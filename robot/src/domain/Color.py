from enum import Enum

from config.config import PUCK_TEMPLATE_LOCATION


class Color(Enum):
    BLACK = 0, PUCK_TEMPLATE_LOCATION + "black.jpg", ([70, 0, 0], [133, 255, 57])
    BROWN = (
        1,
        PUCK_TEMPLATE_LOCATION + "brown.jpg",
        (([4, 68, 0], [18, 255, 72]), ([8, 25, 17], [18, 185, 143])),
    )
    RED = (
        2,
        PUCK_TEMPLATE_LOCATION + "red.jpg",
        (([0, 70, 0], [2, 255, 255]), ([170, 70, 50], [189, 255, 255])),
    )
    ORANGE = (
        3,
        PUCK_TEMPLATE_LOCATION + "orange.jpg",
        ([5, 60, 101], [12, 255, 255]),
    )
    YELLOW = (
        4,
        PUCK_TEMPLATE_LOCATION + "yellow.jpg",
        ([19, 171, 0], [31, 255, 255]),
    )
    GREEN = (
        5,
        PUCK_TEMPLATE_LOCATION + "green.jpg",
        ([48, 105, 39], [79, 255, 255]),
    )
    BLUE = 6, PUCK_TEMPLATE_LOCATION + "blue.jpg", ([103, 0, 0], [126, 255, 255])
    PURPLE = (
        7,
        PUCK_TEMPLATE_LOCATION + "purple.jpg",
        ([114, 0, 10], [158, 109, 255]),
    )
    GREY = (
        8,
        PUCK_TEMPLATE_LOCATION + "grey.jpg",
        ([20, 4, 0], [47, 141, 133]),
    )
    WHITE = 9, PUCK_TEMPLATE_LOCATION + "white.jpg", ([0, 0, 157], [172, 111, 255])
    NONE = 10, "", ([0, 0, 0], [0, 0, 0])
    STARTING_ZONE = (11, "", ([34, 0, 0], [87, 255, 98]))
    INTERIOR_BLUE = (
        12,
        "",
        ([77, 0, 124], [94, 255, 255]),
    )

    def __init__(self, resistance_digit: int, template: str, *hsv_bounds):
        self._resistance_digit = resistance_digit
        self._hsv_bounds = hsv_bounds
        self._template = template

    def get_resistance_digit(self) -> int:
        return self._resistance_digit

    def get_hsv_bounds(self):
        return self._hsv_bounds

    def get_template(self):
        return self._template

    @staticmethod
    def value_of_resistance_digit(digit: int) -> "Color":
        for color in Color:
            if digit == color.get_resistance_digit():
                return color
