from unittest import TestCase

from domain.Orientation import Orientation


class TestOrientation(TestCase):
    AN_ORIENTATION_IN_DEGREE = 53
    ANOTHER_ORIENTATION_IN_DEGREE = 98

    def test_givenTwoEqualOrientations_whenEqual_thenReturnTrue(self):
        an_orientation = Orientation(self.AN_ORIENTATION_IN_DEGREE)

        self.assertEqual(an_orientation, an_orientation)

    def test_givenTwoDifferentOrientation_whenEqual_thenReturnFalse(self):
        an_orientation = Orientation(self.AN_ORIENTATION_IN_DEGREE)
        another_orientation = Orientation(self.ANOTHER_ORIENTATION_IN_DEGREE)

        are_orientations_equal = an_orientation == another_orientation

        self.assertFalse(are_orientations_equal)

    def test_givenAnOrientationInDegree_whenGetOrientationInRadians_thenOrientationIsConvertedCorrectly(self):
        an_orientation = Orientation(self.AN_ORIENTATION_IN_DEGREE)
        expected_orientation_in_radians = 0.9250245035569946

        actual_orientation_in_radians = an_orientation.get_orientation_in_radians()

        self.assertEqual(expected_orientation_in_radians, actual_orientation_in_radians)
