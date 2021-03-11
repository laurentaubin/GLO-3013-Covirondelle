from enum import IntEnum


class ResistanceColor(IntEnum):
    BLACK = 0
    BROWN = 1
    RED = 2
    ORANGE = 3
    YELLOW = 4
    GREEN = 5
    BLUE = 6
    PURPLE = 7
    GREY = 8
    WHITE = 9

    @staticmethod
    def valueOf(single_digit: int) -> "ResistanceColor":
        for resistance_color in ResistanceColor:
            if single_digit == resistance_color.value:
                return resistance_color
