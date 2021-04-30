import unittest

from domain.Position import Position


class TestPosition(unittest.TestCase):
    def setUp(self) -> None:
        self.A_POSITION = Position(20, 30)
        self.ANOTHER_POSITION = Position(40, 7)
        self.NEGATIVE_POSITION = Position(-20, -29)
        self.POSITIVE_POSITION = Position(20, 29)
        self.EXPECTED_SUBSTRACTED_POSITION = Position(-20, 23)
        self.EXPECTED_ADDED_POSITION = Position(60, 37)

    def test_whenSubstracting_thenReturnsCorrectPosition(self):
        actual_position = self.A_POSITION - self.ANOTHER_POSITION
        self.assertEqual(self.EXPECTED_SUBSTRACTED_POSITION, actual_position)

    def test_whenAdding_thenReturnsCorrectPosition(self):
        actual_position = self.A_POSITION + self.ANOTHER_POSITION
        self.assertEqual(self.EXPECTED_ADDED_POSITION, actual_position)

    def test_whenAbsolute_thenReturnsCorrectPosition(self):
        self.assertEqual(abs(self.NEGATIVE_POSITION), self.POSITIVE_POSITION)
