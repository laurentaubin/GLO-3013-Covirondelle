import unittest

from domain.Position import Position
from domain.UnitOfMeasure import UnitOfMeasure


class TestPosition(unittest.TestCase):

    def setUp(self) -> None:
        self.A_POSITION = Position(20, 30)
        self.ANOTHER_POSITION = Position(40, 7)
        self.AN_EQUIVALENT_PIXEL_POSITION = Position(60, 120, UnitOfMeasure.PIXEL)
        self.AN_EQUIVALENT_CENTIMETER_POSITION = Position(10, 20, UnitOfMeasure.CENTIMETERS)
        self.NEGATIVE_POSITION = Position(-20, -29)
        self.POSITIVE_POSITION = Position(20, 29)
        self.EXPECTED_SUBSTRACTED_POSITION = Position(-20, 23)
        self.EXPECTED_ADDED_POSITION = Position(60, 37)
        self.A_PIXEL_POSITION = Position(10, 23, UnitOfMeasure.PIXEL)
        self.A_CENTIMETERS_POSITION = Position(-20, 23, UnitOfMeasure.CENTIMETERS)
        self.A_SUBSTRACTION_EXPECTED_VALUE = Position(130, -115)
        self.ANOTHER_SUBSTRACTION_EXPECTED_VALUE = Position(-130, 115)
        self.AN_ADDITION_EXPECTED_VALUE = Position(-110, 161)

    def test_whenSubstracting_thenReturnsCorrectPosition(self):
        actual_position = self.A_POSITION - self.ANOTHER_POSITION
        self.assertEqual(self.EXPECTED_SUBSTRACTED_POSITION, actual_position)

    def test_whenAdding_thenReturnsCorrectPosition(self):
        actual_position = self.A_POSITION + self.ANOTHER_POSITION
        self.assertEqual(self.EXPECTED_ADDED_POSITION, actual_position)

    def test_whenAbsolute_thenReturnsCorrectPosition(self):
        self.assertEqual(abs(self.NEGATIVE_POSITION), self.POSITIVE_POSITION)

    def test_whenComparingPositionsTwoDifferentTypes_thenReturnCorrectPosition(self):
        self.assertEqual(self.AN_EQUIVALENT_CENTIMETER_POSITION, self.AN_EQUIVALENT_PIXEL_POSITION)
        self.assertEqual(self.AN_EQUIVALENT_PIXEL_POSITION, self.AN_EQUIVALENT_CENTIMETER_POSITION)
        self.assertEqual(self.AN_EQUIVALENT_CENTIMETER_POSITION, self.AN_EQUIVALENT_CENTIMETER_POSITION)
        self.assertEqual(self.AN_EQUIVALENT_PIXEL_POSITION, self.AN_EQUIVALENT_PIXEL_POSITION)

    def test_whenSubstractionTwoPositionsWithDifferentTypes_thenReturnsCorrectPosition(self):
        substraction_result = self.A_PIXEL_POSITION - self.A_CENTIMETERS_POSITION
        another_substraction_result = self.A_CENTIMETERS_POSITION - self.A_PIXEL_POSITION

        self.assertEqual(substraction_result, self.A_SUBSTRACTION_EXPECTED_VALUE)
        self.assertEqual(another_substraction_result, self.ANOTHER_SUBSTRACTION_EXPECTED_VALUE)

    def test_whenAddingTwoPositionsWithDifferentTypes_thenReturnsCorrectPosition(self):
        addition_result = self.A_PIXEL_POSITION + self.A_CENTIMETERS_POSITION
        self.assertEqual(self.AN_ADDITION_EXPECTED_VALUE, addition_result)
