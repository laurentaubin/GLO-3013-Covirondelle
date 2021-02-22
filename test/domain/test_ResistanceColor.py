from unittest import TestCase

from domain.resistance.ResistanceColor import ResistanceColor


class TestResistanceColor(TestCase):
    def test_givenNumberFour_whenGettingValueOf_thenReturnYellow(self):
        single_digit = 4

        resistance_color = ResistanceColor.valueOf(single_digit)

        self.assertEqual(resistance_color, ResistanceColor.YELLOW)

    def test_givenNumberEight_whenGettingValueOf_thenReturnGrey(self):
        single_digit = 8

        resistance_color = ResistanceColor.valueOf(single_digit)

        self.assertEqual(resistance_color, ResistanceColor.GREY)
