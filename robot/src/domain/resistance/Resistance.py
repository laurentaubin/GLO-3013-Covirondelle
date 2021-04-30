from domain.exception.InvalidResistanceException import InvalidResistanceException
from domain.Color import Color


class Resistance:
    E12_RESISTANCE_VALUES = [
        10,
        12,
        15,
        18,
        22,
        27,
        33,
        39,
        47,
        56,
        68,
        82,
    ]

    ORDER_OF_MAGNITUDE_RANGE = [10 ** order for order in range(1, 5)]

    def __init__(self, resistance_value: float) -> None:
        self._resistance_value = resistance_value

    def get_colors(self) -> {Color, Color, Color}:

        first_digit = self.find_nth_digit(0)
        second_digit = self.find_nth_digit(1)
        multiplication_factor = self._find_multiplication_factor()

        return (
            Color.value_of_resistance_digit(first_digit),
            Color.value_of_resistance_digit(second_digit),
            Color.value_of_resistance_digit(multiplication_factor),
        )

    def __eq__(self, other):
        if not isinstance(other, Resistance):
            return False

        return self._resistance_value == other._resistance_value

    @staticmethod
    def round_to_nearest_e12_value(resistance_read: float) -> "Resistance":
        for order_of_magnitude in Resistance.ORDER_OF_MAGNITUDE_RANGE:
            for base_e12_value in Resistance.E12_RESISTANCE_VALUES:
                e12_value = base_e12_value * order_of_magnitude
                lower_bound = e12_value * 0.9
                upper_bound = e12_value * 1.1

                if lower_bound <= resistance_read < upper_bound:
                    return Resistance(e12_value)

        raise InvalidResistanceException

    def find_nth_digit(self, digit: int) -> int:
        return int(str(self._resistance_value)[digit])

    def _find_multiplication_factor(self) -> int:
        order = len(str(self._resistance_value))
        return order - 2
