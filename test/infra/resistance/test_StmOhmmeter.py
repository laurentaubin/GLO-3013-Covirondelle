from unittest import TestCase
from unittest.mock import MagicMock

from infra.resistance.StmOhmmeter import StmOhmmeter


class TestStmOhmmeter(TestCase):
    def setUp(self) -> None:
        self.serial = MagicMock()
        self.stm_ohmmeter = StmOhmmeter(self.serial)

    def test_whenReadResistance_thenSendRightCommandToSTM(self):
        self.serial.readline.return_value = b" 7 1893848.4"
        read_resistance_command = b"\x07"

        self.stm_ohmmeter.read_resistance()

        self.serial.write.assert_called_with(read_resistance_command)

    def test_givenResistanceReturnedByStm_whenReadResistance_thenDecodeAndReturnValue(
        self,
    ):
        self.serial.readline.return_value = b"7 1234.5"
        expected_resistance_value = 1234.5

        actual_resistance = self.stm_ohmmeter.read_resistance()

        self.assertEqual(expected_resistance_value, actual_resistance)
