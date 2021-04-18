from unittest.mock import MagicMock

from serial import Serial

from config.config import (
    CURRENT_CONSUMPTION_THRESHOLD,
    POWER_SENT_TO_WHEELS,
    TIME_BETWEEN_COMMAND,
    TOTAL_CHARGE,
)
from domain.communication.IRobotInformation import IRobotInformation
from domain.communication.StmCommand import StmCommand
from domain.communication.StmPeripherals import StmPeripherals
from domain.gripper.GripperStatus import GripperStatus


class StmRobotInformation(IRobotInformation):
    TOTAL_TIME = 0
    CURRENT_CONSUMPTION_TOTAL = 0

    def __init__(self, serial: Serial):
        self._serial = serial

    def get_gripper_status(self) -> GripperStatus:
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.GRIPPER])
        self._serial.write(command)
        current_consumption = self._serial.readline()[1:].decode("utf-8")
        if float(current_consumption) > CURRENT_CONSUMPTION_THRESHOLD:
            return GripperStatus.HAS_PUCK
        return GripperStatus.DOESNT_HAVE_PUCK

    def get_current_consumption(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.BATTERY])
        self._serial.write(command)
        current_consumption = float(self._serial.readline()[1:].decode("utf-8"))
        return current_consumption

    def get_power_consumption(self):
        command = bytes([StmCommand.ASK_POWER]) + bytes([StmPeripherals.BATTERY])
        self._serial.write(command)
        power_consumption = float(self._serial.readline()[2:].decode("utf-8"))
        return power_consumption

    def get_power_consumption_first_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_1])
        self._serial.write(command)
        current_first_wheel = float(self._serial.readline()[1:].decode("utf-8"))
        power_consumption_first_wheel = self._calculate_wheel_power_consumption(
            current_first_wheel
        )
        return power_consumption_first_wheel

    def get_power_consumption_second_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_2])
        self._serial.write(command)
        current_second_wheel = float(self._serial.readline()[1:].decode("utf-8"))
        power_consumption_second_wheel = self._calculate_wheel_power_consumption(
            current_second_wheel
        )
        return power_consumption_second_wheel

    def get_power_consumption_third_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_3])
        self._serial.write(command)
        current_third_wheel = float(self._serial.readline()[1:].decode("utf-8"))
        power_consumption_third_wheel = self._calculate_wheel_power_consumption(
            current_third_wheel
        )
        return power_consumption_third_wheel

    def get_power_consumption_fourth_wheel(self):
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.MOTOR_4])
        self._serial.write(command)
        current_fourth_wheel = float(self._serial.readline()[1:].decode("utf-8"))
        power_consumption_fourth_wheel = self._calculate_wheel_power_consumption(
            current_fourth_wheel
        )
        return power_consumption_fourth_wheel

    def get_battery_time_left(self):
        self.TOTAL_TIME += 1
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.BATTERY])
        self._serial.write(command)
        current_consumption = float(self._serial.readline()[1:].decode("utf-8"))

        self.CURRENT_CONSUMPTION_TOTAL += current_consumption
        current_consumption_average = (
            self.CURRENT_CONSUMPTION_TOTAL / self.TOTAL_TIME * TIME_BETWEEN_COMMAND
        )

        actual_charge = TOTAL_CHARGE - current_consumption_average * self.TOTAL_TIME
        battery_time_left = actual_charge / current_consumption_average

        return battery_time_left

    def get_battery_percentage(self):
        current_consumption_average = (
            self.CURRENT_CONSUMPTION_TOTAL * TIME_BETWEEN_COMMAND
        )
        battery_percent = (
            (TOTAL_CHARGE - current_consumption_average) / TOTAL_CHARGE
        ) * 100

        return battery_percent

    def _calculate_wheel_power_consumption(self, wheel_current):
        return (wheel_current / 1000) * POWER_SENT_TO_WHEELS
