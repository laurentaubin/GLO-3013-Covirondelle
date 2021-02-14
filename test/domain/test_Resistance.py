from unittest import TestCase

from domain.Resistance import Resistance
from domain.ResistanceColor import ResistanceColor


class TestResistance(TestCase):
    def test_givenResistanceValueStartingWithFour_whenGettingColors_thenFirstColorIsYellow(
        self,
    ):
        resistance = Resistance(450)

        first_color, *_ = resistance.getColors()

        self.assertEqual(first_color, ResistanceColor.YELLOW)

    def test_givenResistanceValueStartingWithFive_whenGettingColors_thenFirstColorIsGreen(
        self,
    ):
        resistance = Resistance(550)

        first_color, *_ = resistance.getColors()

        self.assertEqual(first_color, ResistanceColor.GREEN)

    def test_givenResistanceValueWithTwoAsSecondDigit_whenGettingColors_thenSecondColorIsRed(
        self,
    ):
        resistance = Resistance(120)

        _, second_color, *_ = resistance.getColors()

        self.assertEqual(second_color, ResistanceColor.RED)

    def test_givenResistanceValueWithSixAsSecondDigit_whenGettingColors_thenSecondColorIsBlue(
        self,
    ):
        resistance = Resistance(160)

        _, second_color, *_ = resistance.getColors()

        self.assertEqual(second_color, ResistanceColor.BLUE)

    def test_givenResistanceValueOfOrderFive_whenGettingColors_thenThirdColorIsOrange(
        self,
    ):
        resistance = Resistance(25000)

        *_, third_color = resistance.getColors()

        self.assertEqual(third_color, ResistanceColor.ORANGE)

    def test_givenResistanceValueOfOrderThree_whenGettingColors_thenThirdColorIsBrown(
        self,
    ):
        resistance = Resistance(840)

        *_, third_color = resistance.getColors()

        self.assertEqual(third_color, ResistanceColor.BROWN)
