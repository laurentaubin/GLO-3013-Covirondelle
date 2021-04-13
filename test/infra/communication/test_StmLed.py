from unittest import TestCase
from unittest.mock import MagicMock

from infra.communication.robot_information.StmLed import StmLed


class TestStmLed(TestCase):
    def setUp(self) -> None:
        self.serial = MagicMock()
        self.led_information = StmLed(self.serial)

    def test_givenAToggleLedCommand_whenToggleLed_thenTheRightCommandIsSent(self):
        expected_command = b"\x0B"

        self.led_information.toggle_led()

        self.serial.write.assert_called_with(expected_command)

    def test_givenAToggleLedCommand_whenGetLedStatus_thenRightValueIsReturned(self):
        expected_toggle_value = True
        self.led_information.toggle_led()

        actual_toggle_value = self.led_information.get_led_status()

        self.assertEqual(expected_toggle_value, actual_toggle_value)
