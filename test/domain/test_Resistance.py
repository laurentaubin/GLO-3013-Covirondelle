from unittest import TestCase

from domain.exception.InvalidResistanceException import InvalidResistanceException
from domain.resistance.Resistance import Resistance
from domain.Color import Color


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

    def test_givenResistanceValueOf9500_whenRoundToNearestE12Value_thenReturnClosestE12ValueOf10000(
        self,
    ):
        resistance_read = 9500
        expected_resistance = Resistance(10000)

        actual_resistance = Resistance.round_to_nearest_e12_value(resistance_read)

        self.assertEqual(expected_resistance, actual_resistance)

    def test_givenResistanceValueOf31000_whenRoundToNearestE12Value_thenReturnClosestE12ValueOf33000(
        self,
    ):
        resistance_read = 31000
        expected_resistance = Resistance(33000)

        actual_resistance = Resistance.round_to_nearest_e12_value(resistance_read)

        self.assertEqual(expected_resistance, actual_resistance)

    def test_givenResistanceValueOf50_whenRoundToNearestE12Value_thenThrowInvalidResistanceException(
        self,
    ):
        resistance_read = 50

        rounding_to_nearest_e12_value = (
            lambda resistance: Resistance.round_to_nearest_e12_value(resistance)
        )

        with self.assertRaises(InvalidResistanceException):
            rounding_to_nearest_e12_value(resistance_read)

    def test_givenResistanceValueOf500000_whenRoundToNearestE12Value_thenThrowInvalidResistanceException(
        self,
    ):
        resistance_read = 500000

        rounding_to_nearest_e12_value = (
            lambda resistance: Resistance.round_to_nearest_e12_value(resistance)
        )

        with self.assertRaises(InvalidResistanceException):
            rounding_to_nearest_e12_value(resistance_read)
