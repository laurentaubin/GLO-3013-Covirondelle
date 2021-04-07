from unittest import TestCase
from unittest.mock import MagicMock

from domain.Position import Position
from domain.StartingZone import StartingZone
from domain.StartingZoneCorner import StartingZoneCorner


class TestStartingZone(TestCase):
    A_POSITION = MagicMock()
    UPPER_LEFT_CORNER = Position(23, 23)
    UPPER_RIGHT_CORNER = Position(500, 23)
    LOWER_LEFT_CORNER = Position(23, 500)
    LOWER_RIGHT_CORNER = Position(500, 500)
    STARTING_ZONE_CENTER = Position(426, 449)

    def setUp(self) -> None:
        self.starting_zone = StartingZone(
            [
                self.UPPER_RIGHT_CORNER,
                self.UPPER_LEFT_CORNER,
                self.LOWER_LEFT_CORNER,
                self.LOWER_RIGHT_CORNER,
            ],
            self.STARTING_ZONE_CENTER,
        )

    def test_whenInstantiatingStartingZone_thenCornersAreSorted(self):
        starting_zone = StartingZone(
            [
                self.LOWER_RIGHT_CORNER,
                self.LOWER_LEFT_CORNER,
                self.UPPER_RIGHT_CORNER,
                self.UPPER_LEFT_CORNER,
            ],
            self.STARTING_ZONE_CENTER,
        )

        self.assertEqual(self.UPPER_LEFT_CORNER, starting_zone._upper_left_corner)
        self.assertEqual(self.UPPER_RIGHT_CORNER, starting_zone._upper_right_corner)
        self.assertEqual(self.LOWER_LEFT_CORNER, starting_zone._lower_left_corner)
        self.assertEqual(self.LOWER_RIGHT_CORNER, starting_zone._lower_right_corner)

    def test_givenLetterA_whenFindCornerPositionFromLetter_thenReturnUpperLeftCorner(
        self,
    ):

        corner_position = self.starting_zone.find_corner_position_from_letter(
            StartingZoneCorner.A
        )

        self.assertEqual(self.UPPER_RIGHT_CORNER, corner_position)

    def test_givenLetterB_whenFindCornerPositionFromLetter_thenReturnUpperRightCorner(
        self,
    ):
        corner_position = self.starting_zone.find_corner_position_from_letter(
            StartingZoneCorner.B
        )

        self.assertEqual(self.LOWER_RIGHT_CORNER, corner_position)

    def test_givenLetterC_whenFindCornerPositionFromLetter_thenReturnLowerRightCorner(
        self,
    ):
        corner_position = self.starting_zone.find_corner_position_from_letter(
            StartingZoneCorner.C
        )

        self.assertEqual(self.LOWER_LEFT_CORNER, corner_position)

    def test_givenLetterD_whenFindCornerPositionFromLetter_thenReturnLowerLeftCorner(
        self,
    ):
        corner_position = self.starting_zone.find_corner_position_from_letter(
            StartingZoneCorner.D
        )

        self.assertEqual(self.UPPER_LEFT_CORNER, corner_position)
