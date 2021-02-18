from unittest import TestCase

from domain.Position import Position
from domain.StartingZone import StartingZone


class TestStartingZone(TestCase):
    def test_whenInstantiatingStartingZone_thenCornersAreSorted(self):
        upper_left_corner = Position(23, 23)
        upper_right_corner = Position(500, 23)
        lower_left_corner = Position(23, 500)
        lower_right_corner = Position(500, 500)

        starting_zone = StartingZone(
            [
                lower_right_corner,
                lower_left_corner,
                upper_right_corner,
                upper_left_corner,
            ]
        )

        self.assertEqual(upper_left_corner, starting_zone._upper_left_corner)
        self.assertEqual(upper_right_corner, starting_zone._upper_right_corner)
        self.assertEqual(lower_left_corner, starting_zone._lower_left_corner)
        self.assertEqual(lower_right_corner, starting_zone._lower_right_corner)
