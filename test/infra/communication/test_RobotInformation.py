from unittest import TestCase
from unittest.mock import MagicMock

from domain.gripper.GripperStatus import GripperStatus
from infra.communication.robot_information.StmRobotInformation import (
    StmRobotInformation,
)


class TestRobotInformation(TestCase):
    def setUp(self) -> None:
        self.serial = MagicMock()
        self.robot_information = StmRobotInformation(self.serial)

    def test_givenCurrentConsumptionAbove200_whenGetGripperStatus_thenGripperHasPuck(
        self,
    ):
        a_current_value = "250"
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            a_current_value, encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_gripper_status = self.robot_information.get_gripper_status()

        self.assertEqual(GripperStatus.HAS_PUCK, actual_gripper_status)

    def test_givenCurrentConsumptionUnder200_whenGetGripperStatus_thenGripperDoesntHavePuck(
        self,
    ):
        a_current_value = "100"
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            a_current_value, encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_gripper_status = self.robot_information.get_gripper_status()

        self.assertEqual(GripperStatus.DOESNT_HAVE_PUCK, actual_gripper_status)

    def test_givenAReadGripperCurrentCommand_whenGetGripperStatus_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x08\x05"

        self.robot_information.get_gripper_status()

        self.serial.write.assert_called_with(expected_command)

    def test_givenAReadCurrentConsumptionCommand_whenGetCurrentConsumption_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x08\x00"

        self.robot_information.get_current_consumption()

        self.serial.write.assert_called_with(expected_command)

    def test_givenAReadLineCurrentConsumptionValue_whenGetCurrentConsumption_thenTheRightValueIsReturned(
        self,
    ):
        expected_current_consumption_value = 10.0
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_current_consumption = self.robot_information.get_current_consumption()

        self.assertEqual(expected_current_consumption_value, actual_current_consumption)

    def test_givenAReadPowerConsumptionCommand_whenGetConsumptionStatus_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x0A\x00"

        self.robot_information.get_power_consumption()

        self.serial.write.assert_called_with(expected_command)

    def test_givenAReadLinePowerConsumptionValue_whenGetPowerConsumption_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_value = 10.0
        expected_serial_response = bytes("0A", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_power_consumption = self.robot_information.get_power_consumption()

        self.assertEqual(expected_power_consumption_value, actual_power_consumption)
