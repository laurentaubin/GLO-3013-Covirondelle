from domain.Color import Color


class Resistance:
    def __init__(self, resistance_value: int) -> None:
        self._resistance_value = resistance_value

    def get_value(self) -> int:
        return self._resistance_value

    def get_colors(self) -> {Color, Color, Color}:

        first_digit = self._find_nth_digit(0)
        second_digit = self._find_nth_digit(1)
        multiplication_factor = self._find_multiplication_factor()

        return (
            Color.value_of_resistance_digit(first_digit),
            Color.value_of_resistance_digit(second_digit),
            Color.value_of_resistance_digit(multiplication_factor),
        )

    def _find_nth_digit(self, digit: int) -> int:
        return int(str(self._resistance_value)[digit])

    def _find_multiplication_factor(self) -> int:
        order = len(str(self._resistance_value))
        return order - 2
