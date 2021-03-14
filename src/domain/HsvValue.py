from enum import Enum


class HsvValue(Enum):
    BROWN = ([6, 63, 0], [23, 255, 81])
    GREY = ([23, 0, 0], [80, 105, 107])
    WHITE = ([37, 0, 131], [170, 25, 152])
    BLACK = ([0, 0, 0], [179, 255, 21])
    RED = ([0, 123, 40], [5, 255, 114])
    YELLOW = ([20, 100, 100], [30, 255, 255])
    BLUE = ([80, 160, 20], [120, 255, 255])
    GREEN = ([48, 105, 39], [79, 255, 255])
    ORANGE = ([4, 103, 100], [15, 255, 255])
    PURPLE = ([119, 37, 95], [176, 84, 138])

    def get_lower_bound(self):
        return self.value[0]

    def get_upper_bound(self):
        return self.value[1]
