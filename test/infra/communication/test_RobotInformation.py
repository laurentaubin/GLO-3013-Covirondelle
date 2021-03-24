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

    def test_givenCurrentConsumptionAbove300_whenGetGripperStatus_thenGripperHasPuck(
        self,
    ):
        a_current_value = "400"
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            a_current_value, encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_gripper_status = self.robot_information.get_gripper_status()

        self.assertEqual(GripperStatus.HAS_PUCK, actual_gripper_status)

    def test_givenCurrentConsumptionUnder300_whenGetGripperStatus_thenGripperDoesntHavePuck(
        self,
    ):
        a_current_value = "200"
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
