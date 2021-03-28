from unittest import TestCase

from domain.UnitOfMeasure import UnitOfMeasure
from domain.movement.Distance import Distance


class TestDistance(TestCase):
    def test_givenNoUnitOfMeasureSpecified_whenCreateDistance_thenUnitOfMeasureIsPixel(
        self,
    ):
        expected_distance = Distance(200)

        actual_distance = Distance(200, unit_of_measure=UnitOfMeasure.PIXEL)

        self.assertEqual(expected_distance, actual_distance)

    def test_givenPixelUnitOfMeasure_whenCreateDistance_thenDistanceIsConvertedToMeter(
        self,
    ):
        expected_distance_value = 2

        actual_distance = Distance(1286, unit_of_measure=UnitOfMeasure.PIXEL)

        self.assertEqual(expected_distance_value, actual_distance.get_distance())

    def test_givenDistanceInPixels_whenCreateEquivalentDistanceInMeters_thenDistancesAreEqual(
        self,
    ):
        pixel_distance = Distance(321.5, unit_of_measure=UnitOfMeasure.PIXEL)

        meter_distance = Distance(0.5, unit_of_measure=UnitOfMeasure.METER)

        self.assertEqual(pixel_distance, meter_distance)
