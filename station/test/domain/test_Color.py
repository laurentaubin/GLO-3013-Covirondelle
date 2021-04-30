from unittest import TestCase

from domain.Color import Color


class TestColor(TestCase):
    def test_givenNumberFour_whenGettingValueOfResistanceDigit_thenReturnYellow(self):
        single_digit = 4

        color = Color.value_of_resistance_digit(single_digit)

        self.assertEqual(color, Color.YELLOW)

    def test_givenNumberEight_whenGettingValueOfResistanceDigit_thenReturnGrey(self):
        single_digit = 8

        color = Color.value_of_resistance_digit(single_digit)

        self.assertEqual(color, Color.GREY)
