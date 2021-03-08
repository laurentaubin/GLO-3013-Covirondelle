from unittest import TestCase

from domain.movement.CommandDuration import CommandDuration
from domain.movement.Distance import Distance
from domain.movement.Speed import Speed


class TestSpeed(TestCase):
    A_DISTANCE_VALUE = 10.5
    A_DURATION_VALUE = 5.2

    def test_whenCalculateFromDistanceAndDuration_thenReturnSpeedWithValueDistanceDividedByDuration(
        self,
    ):
        a_distance = Distance(self.A_DISTANCE_VALUE)
        a_duration = CommandDuration(self.A_DURATION_VALUE)
        expected_speed_value = self.A_DISTANCE_VALUE / self.A_DURATION_VALUE

        actual_speed = Speed.calculate_from_distance_and_duration(
            a_distance, a_duration
        )

        self.assertEqual(expected_speed_value, actual_speed.get_speed())
