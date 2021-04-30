from infra.communication import ThreadSafeSerial

from domain.communication.StmCommand import StmCommand
from domain.resistance.IOhmmeter import IOhmmeter


class StmOhmmeter(IOhmmeter):
    def __init__(self, serial: ThreadSafeSerial):
        self._serial = serial

    def read_resistance(self) -> float:
        read_resistance_command = bytes([StmCommand.READ_RESISTANCE])

        response = self._serial.write_and_readline(read_resistance_command)

        _header, resistance_value = response.decode("utf-8").split()
        return float(resistance_value)
