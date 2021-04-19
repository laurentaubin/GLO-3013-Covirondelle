from unittest import TestCase
from unittest.mock import MagicMock

from domain.gripper.GripperStatus import GripperStatus
from infra.communication.robot_information.StmRobotInformation import (
    StmRobotInformation,
)


class TestStmRobotInformation(TestCase):
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
        self.serial.write_and_readline.return_value = expected_serial_response

        actual_gripper_status = self.robot_information.get_gripper_status()

        self.assertEqual(GripperStatus.HAS_PUCK, actual_gripper_status)

    def test_givenCurrentConsumptionUnder200_whenGetGripperStatus_thenGripperDoesntHavePuck(
        self,
    ):
        a_current_value = "100"
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            a_current_value, encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response

        actual_gripper_status = self.robot_information.get_gripper_status()

        self.assertEqual(GripperStatus.DOESNT_HAVE_PUCK, actual_gripper_status)

    def test_givenAReadGripperCurrentCommand_whenGetGripperStatus_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x08\x05"

        self.robot_information.get_gripper_status()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAReadCurrentConsumptionCommand_whenGetCurrentConsumption_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x08\x00"

        self.robot_information.get_current_consumption()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenACurrentConsumptionValue_whenGetCurrentConsumption_thenTheRightValueIsReturned(
        self,
    ):
        expected_current_consumption_value = 10.0
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response

        actual_current_consumption = self.robot_information.get_current_consumption()

        self.assertEqual(expected_current_consumption_value, actual_current_consumption)

    def test_givenAReadPowerConsumptionCommand_whenGetConsumptionStatus_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x0A\x00"

        self.robot_information.get_power_consumption()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAPowerConsumptionValue_whenGetPowerConsumption_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_value = 10.0
        expected_serial_response = bytes("0A", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response

        actual_power_consumption = self.robot_information.get_power_consumption()

        self.assertEqual(expected_power_consumption_value, actual_power_consumption)

    def test_givenAReadPowerConsumptionFirstWheelCommand_whenGetConsumptionFirstWheel_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = expected_command = b"\x08\x01"

        self.robot_information.get_power_consumption_first_wheel()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAReadLinePowerConsumptionFirstWheelValue_whenGetPowerConsumptionFirstWheel_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_first_wheel_value = 1.02
        expected_serial_response = bytes("08", encoding="utf-8") + bytes(
            "5", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response
        actual_power_consumption_first_wheel = (
            self.robot_information.get_power_consumption_first_wheel()
        )
        self.assertEqual(
            expected_power_consumption_first_wheel_value,
            actual_power_consumption_first_wheel,
        )

    def test_givenAReadPowerConsumptionSecondWheelCommand_whenGetConsumptionSecondWheel_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = expected_command = b"\x08\x02"

        self.robot_information.get_power_consumption_second_wheel()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAReadLinePowerConsumptionSecondWheelValue_whenGetPowerConsumptionSecondWheel_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_second_wheel_value = 1.02
        expected_serial_response = bytes("08", encoding="utf-8") + bytes(
            "5", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response
        actual_power_consumption_second_wheel = (
            self.robot_information.get_power_consumption_second_wheel()
        )
        self.assertEqual(
            expected_power_consumption_second_wheel_value,
            actual_power_consumption_second_wheel,
        )

    def test_givenAReadPowerConsumptionThirdWheelCommand_whenGetConsumptionThirdWheel_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = expected_command = b"\x08\x03"

        self.robot_information.get_power_consumption_third_wheel()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAReadLinePowerConsumptionThirdWheelValue_whenGetPowerConsumptionThirdWheel_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_third_wheel_value = 1.02
        expected_serial_response = bytes("08", encoding="utf-8") + bytes(
            "5", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response
        actual_power_consumption_third_wheel = (
            self.robot_information.get_power_consumption_third_wheel()
        )
        self.assertEqual(
            expected_power_consumption_third_wheel_value,
            actual_power_consumption_third_wheel,
        )

    def test_givenAReadPowerConsumptionFourthWheelCommand_whenGetConsumptionFourthWheel_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = expected_command = b"\x08\x04"

        self.robot_information.get_power_consumption_fourth_wheel()

        self.serial.write_and_readline.assert_called_with(expected_command)

    def test_givenAReadLinePowerConsumptionFourthWheelValue_whenGetPowerConsumptionFourthWheel_thenTheRightValueIsReturned(
        self,
    ):
        expected_power_consumption_fourth_wheel_value = 1.02
        expected_serial_response = bytes("08", encoding="utf-8") + bytes(
            "5", encoding="utf-8"
        )
        self.serial.write_and_readline.return_value = expected_serial_response
        actual_power_consumption_fourth_wheel = (
            self.robot_information.get_power_consumption_fourth_wheel()
        )
        self.assertEqual(
            expected_power_consumption_fourth_wheel_value,
            actual_power_consumption_fourth_wheel,
        )

    def test_givenAReadCurrentCommand_whenGetBatteryTimeLeft_thenTheRightCommandIsSent(
        self,
    ):
        expected_command = b"\x08\x00"

        self.robot_information.get_battery_time_left()

        self.serial.write.assert_called_with(expected_command)

    def test_givenAReadLineCurrentValue_whenGetBatteryTimeLeft_thenTheRightValueIsReturned(
        self,
    ):
        expected_time_left = 2159999.0
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        actual_time_left = self.robot_information.get_battery_time_left()

        self.assertEqual(expected_time_left, actual_time_left)

    def test_givenASecondCurrentConsumptionCall_whenGetBatteryPercentage_thenValueIsLowerThan100(
        self,
    ):
        expected_serial_response = bytes("8", encoding="utf-8") + bytes(
            "10", encoding="utf-8"
        )
        self.serial.readline.return_value = expected_serial_response

        self.robot_information.get_battery_time_left()
        expected_battery_percentage = 99.99995370370371

        actual_battery_percentage = self.robot_information.get_battery_percentage()

        self.assertEqual(expected_battery_percentage, actual_battery_percentage)
