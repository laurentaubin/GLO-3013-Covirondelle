from unittest import TestCase

from domain.Color import Color


class TestColor(TestCase):
    def test_givenNumberFour_whenGettingValueOf_thenReturnYellow(self):
        single_digit = 4

        resistance_color = Color.value_of_resistance_digit(single_digit)

        self.assertEqual(resistance_color, Color.YELLOW)

    def test_givenNumberEight_whenGettingValueOf_thenReturnGrey(self):
        single_digit = 8

        resistance_color = Color.value_of_resistance_digit(single_digit)

        self.assertEqual(resistance_color, Color.GREY)
