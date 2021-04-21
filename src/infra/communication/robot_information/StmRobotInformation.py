from infra.communication import ThreadSafeSerial

from config.config import (
    CURRENT_CONSUMPTION_THRESHOLD,
    POWER_SENT_TO_WHEELS,
    TOTAL_CHARGE,
    TIME_BETWEEN_COMMAND,
    MOLSON_A,
    MOLSON_B,
)
from domain.communication.IRobotInformation import IRobotInformation
from domain.communication.StmCommand import StmCommand
from domain.communication.StmPeripherals import StmPeripherals
from domain.gripper.GripperStatus import GripperStatus


class StmRobotInformation(IRobotInformation):
    def __init__(
        self, serial: ThreadSafeSerial, total_time=0, current_consumption_total=0
    ):
        self._serial = serial
        self.total_time = total_time
        self.current_consumption_total = current_consumption_total

    def get_gripper_status(self) -> GripperStatus:
        consumptions = list()
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.GRIPPER])
        for i in range(10):
            response = self._serial.write_and_readline(command)
            consumptions.append(float(response[1:].decode("utf-8")))
        current_consumption = sum(consumptions) / len(consumptions)
        if current_consumption > CURRENT_CONSUMPTION_THRESHOLD:
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
        print(float(power_consumption) / 1000)
        return float(power_consumption) / 1000

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

    def get_battery_time_left(self):
        self.total_time += 1
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.BATTERY])
        response = self._serial.write_and_readline(command)

        current_consumption = float(response[1:].decode("utf-8"))
        battery_percentage = self.get_battery_percentage()

        self.current_consumption_total += current_consumption
        current_consumption_average = (
            self.current_consumption_total / self.total_time * TIME_BETWEEN_COMMAND
        )

        actual_charge = (
            TOTAL_CHARGE * battery_percentage
        ) / 100 - current_consumption_average * self.total_time
        battery_time_left = actual_charge / current_consumption_average
        return battery_time_left

    def get_battery_percentage(self):
        command = bytes([StmCommand.ASK_VOLTAGE]) + bytes([StmPeripherals.BATTERY])
        response = self._serial.write_and_readline(command)

        battery_voltage = float(response[1:].decode("utf-8"))

        battery_percentage = MOLSON_A * battery_voltage + MOLSON_B
        if battery_percentage > 100:
            battery_percentage = 100.0
        return battery_percentage

    def _calculate_wheel_power_consumption(self, wheel_current):
        return (wheel_current / 1000) * POWER_SENT_TO_WHEELS
