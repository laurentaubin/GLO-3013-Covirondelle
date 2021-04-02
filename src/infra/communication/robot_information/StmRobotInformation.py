from serial import Serial

from config.config import CURRENT_CONSUMPTION_THRESHOLD
from domain.communication.IRobotInformation import IRobotInformation
from domain.communication.StmCommand import StmCommand
from domain.communication.StmPeripherals import StmPeripherals
from domain.gripper.GripperStatus import GripperStatus


class StmRobotInformation(IRobotInformation):
    def __init__(self, serial: Serial):
        self._serial = serial

    def get_gripper_status(self) -> GripperStatus:
        command = bytes([StmCommand.ASK_CURRENT]) + bytes([StmPeripherals.GRIPPER])
        self._serial.write(command)
        current_consumption = self._serial.readline()[1:].decode("utf-8")
        if float(current_consumption) > CURRENT_CONSUMPTION_THRESHOLD:
            return GripperStatus.HAS_PUCK
        return GripperStatus.DOESNT_HAVE_PUCK

    def get_power_consumption(self):
        command = bytes([StmCommand.ASK_POWER]) + bytes([StmPeripherals.BATTERY])
        self._serial.write(command)
        power_consumption = self._serial.readline()[2:].decode("utf-8")
        return power_consumption
