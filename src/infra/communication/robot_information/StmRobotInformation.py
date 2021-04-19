from infra.communication import ThreadSafeSerial

from config.config import CURRENT_CONSUMPTION_THRESHOLD, POWER_SENT_TO_WHEELS
from domain.communication.IRobotInformation import IRobotInformation
from domain.communication.StmCommand import StmCommand
from domain.communication.StmPeripherals import StmPeripherals
from domain.gripper.GripperStatus import GripperStatus


class StmRobotInformation(IRobotInformation):
    def __init__(self, serial: ThreadSafeSerial):
        self._serial = serial

    def get_gripper_status(self) -> GripperStatus:
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.GRIPPER])
        response = self._serial.write_and_readline(command)
        current_consumption = response[1:].decode("utf-8")
        if float(current_consumption) > CURRENT_CONSUMPTION_THRESHOLD:
            return GripperStatus.HAS_PUCK
        return GripperStatus.DOESNT_HAVE_PUCK

    def get_current_consumption(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.BATTERY])
        response = self._serial.write_and_readline(command)
        current_consumption = response[1:].decode("utf-8")
        return float(current_consumption)

    def get_power_consumption(self):
        command = bytes([StmCommand.ASK_POWER]) + bytes([StmPeripherals.BATTERY])
        response = self._serial.write_and_readline(command)
        power_consumption = response[2:].decode("utf-8")
        return float(power_consumption)

    def get_power_consumption_first_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_1])
        response = self._serial.write_and_readline(command)
        current_first_wheel = float(response[1:].decode("utf-8"))
        power_consumption_first_wheel = self._calculate_wheel_power_consumption(
            current_first_wheel
        )
        return power_consumption_first_wheel

    def get_power_consumption_second_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_2])
        response = self._serial.write_and_readline(command)
        current_second_wheel = float(response[1:].decode("utf-8"))
        power_consumption_second_wheel = self._calculate_wheel_power_consumption(
            current_second_wheel
        )
        return power_consumption_second_wheel

    def get_power_consumption_third_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_3])
        response = self._serial.write_and_readline(command)
        current_third_wheel = float(response[1:].decode("utf-8"))
        power_consumption_third_wheel = self._calculate_wheel_power_consumption(
            current_third_wheel
        )
        return power_consumption_third_wheel

    def get_power_consumption_fourth_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_4])
        response = self._serial.write_and_readline(command)
        current_fourth_wheel = float(response[1:].decode("utf-8"))
        power_consumption_fourth_wheel = self._calculate_wheel_power_consumption(
            current_fourth_wheel
        )
        return power_consumption_fourth_wheel

    def _calculate_wheel_power_consumption(self, wheel_current):
        return (wheel_current / 1000) * POWER_SENT_TO_WHEELS
