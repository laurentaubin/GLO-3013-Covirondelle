from domain.ResistanceColor import ResistanceColor


class Resistance:
    def __init__(self, resistance_value: int) -> None:
        self._resistance_value = resistance_value

    def getColors(self) -> {ResistanceColor, ResistanceColor, ResistanceColor}:

        first_digit = self._find_nth_digit(0)
        second_digit = self._find_nth_digit(1)
        multiplication_factor = self._find_multiplication_factor()

        return (
            ResistanceColor.valueOf(first_digit),
            ResistanceColor.valueOf(second_digit),
            ResistanceColor.valueOf(multiplication_factor),
        )

    def _find_nth_digit(self, digit: int) -> int:
        return int(str(self._resistance_value)[digit])

    def _find_multiplication_factor(self) -> int:
        order = len(str(self._resistance_value))
        return order - 2
