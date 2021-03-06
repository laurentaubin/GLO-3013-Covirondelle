from unittest import TestCase

from domain.Color import Color
from domain.resistance.Resistance import Resistance


class TestResistance(TestCase):
    def test_givenResistanceValueStartingWithFour_whenGettingColors_thenFirstColorIsYellow(
        self,
    ):
        resistance = Resistance(450)

        first_color, *_ = resistance.get_colors()

        self.assertEqual(first_color, Color.YELLOW)

    def test_givenResistanceValueStartingWithFive_whenGettingColors_thenFirstColorIsGreen(
        self,
    ):
        resistance = Resistance(550)

        first_color, *_ = resistance.get_colors()

        self.assertEqual(first_color, Color.GREEN)

    def test_givenResistanceValueWithTwoAsSecondDigit_whenGettingColors_thenSecondColorIsRed(
        self,
    ):
        resistance = Resistance(120)

        _, second_color, *_ = resistance.get_colors()

        self.assertEqual(second_color, Color.RED)

    def test_givenResistanceValueWithSixAsSecondDigit_whenGettingColors_thenSecondColorIsBlue(
        self,
    ):
        resistance = Resistance(160)

        _, second_color, *_ = resistance.get_colors()

        self.assertEqual(second_color, Color.BLUE)

    def test_givenResistanceValueOfOrderFive_whenGettingColors_thenThirdColorIsOrange(
        self,
    ):
        resistance = Resistance(25000)

        *_, third_color = resistance.get_colors()

        self.assertEqual(third_color, Color.ORANGE)

    def test_givenResistanceValueOfOrderThree_whenGettingColors_thenThirdColorIsBrown(
        self,
    ):
        resistance = Resistance(840)

        *_, third_color = resistance.get_colors()

        self.assertEqual(third_color, Color.BROWN)
