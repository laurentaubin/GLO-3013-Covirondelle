from serial import Serial

from domain.communication.StmCommand import StmCommand
from domain.resistance.IOhmmeter import IOhmmeter


class StmOhmmeter(IOhmmeter):
    def __init__(self, serial: Serial):
        self._serial = serial

    def read_resistance(self) -> float:
        read_resistance_command = bytes([StmCommand.READ_RESISTANCE])

        self._serial.write(read_resistance_command)

        _header, resistance_value = self._serial.readline().decode("utf-8").split()
        return float(resistance_value)
