from unittest import TestCase
from unittest.mock import MagicMock

from domain.resistance.Resistance import Resistance
from service.resistance.ResistanceService import ResistanceService


class TestResistanceService(TestCase):
    RESISTANCE_THRESHOLD = 100000
    RESISTANCE_ABOVE_THRESHOLD = 120000
    RESISTANCE_BELOW_THRESHOLD = 1500

    def setUp(self) -> None:
        self.ohmmeter = MagicMock()
        self.resistance_service = ResistanceService(
            self.RESISTANCE_THRESHOLD, self.ohmmeter
        )

    def test_givenReadResistanceAboveThreshold_whenConfirmContact_thenReturnFalse(self):
        self.ohmmeter.read_resistance.return_value = self.RESISTANCE_ABOVE_THRESHOLD

        is_contact_confirmed = self.resistance_service.confirm_contact()

        self.assertFalse(is_contact_confirmed)

    def test_givenReadResistanceBelowThreshold_whenConfirmContact_thenReturnTrue(self):
        self.ohmmeter.read_resistance.return_value = self.RESISTANCE_BELOW_THRESHOLD

        is_contact_confirmed = self.resistance_service.confirm_contact()

        self.assertTrue(is_contact_confirmed)

    def test_whenTakeResistanceMeasurement_thenReturnResistanceWithValueRead(self):
        self.ohmmeter.read_resistance.return_value = self.RESISTANCE_ABOVE_THRESHOLD
        expected_resistance = Resistance(self.RESISTANCE_ABOVE_THRESHOLD)

        actual_resistance = self.resistance_service.take_resistance_measurement()

        self.assertEqual(expected_resistance, actual_resistance)
