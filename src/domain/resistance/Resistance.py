from domain.exception.InvalidResistanceException import InvalidResistanceException
from domain.resistance.ResistanceColor import ResistanceColor


class Resistance:
    E12_RESISTANCE_VALUES = [
        10000,
        12000,
        15000,
        18000,
        22000,
        27000,
        33000,
        39000,
        47000,
        56000,
        68000,
        82000,
    ]

    def __init__(self, resistance_value: float) -> None:
        self._resistance_value = resistance_value

    def get_colors(self) -> {ResistanceColor, ResistanceColor, ResistanceColor}:

        first_digit = self._find_nth_digit(0)
        second_digit = self._find_nth_digit(1)
        multiplication_factor = self._find_multiplication_factor()

        return (
            ResistanceColor.valueOf(first_digit),
            ResistanceColor.valueOf(second_digit),
            ResistanceColor.valueOf(multiplication_factor),
        )

    def __eq__(self, other):
        if not isinstance(other, Resistance):
            return False

        return self._resistance_value == other._resistance_value

    @staticmethod
    def round_to_nearest_e12_value(resistance_read: float) -> "Resistance":
        for e12_value in Resistance.E12_RESISTANCE_VALUES:
            lower_bound = e12_value * 0.9
            upper_bound = e12_value * 1.1

            if lower_bound <= resistance_read < upper_bound:
                return Resistance(e12_value)

        raise InvalidResistanceException

    def _find_nth_digit(self, digit: int) -> int:
        return int(str(self._resistance_value)[digit])

    def _find_multiplication_factor(self) -> int:
        order = len(str(self._resistance_value))
        return order - 2
