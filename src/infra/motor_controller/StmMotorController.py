import struct
from typing import List

from serial import Serial, time

from domain.IMotorController import IMotorController
from domain.movement.MovementCommand import MovementCommand


class StmMotorController(IMotorController):
    def __init__(self, serial: Serial) -> None:
        self._serial = serial

    def actuate_wheels(self, commands: List[MovementCommand]) -> None:
        for command in commands:
            self._send_command_to_motor(command)

    def _send_command_to_motor(self, command: MovementCommand):
        print(
            "Sending command with direction %s, speed %f and duration %f"
            % (
                command.get_direction().name,
                command.get_speed().get_speed(),
                command.get_duration().get_duration(),
            )
        )

        encoded_direction = bytes(([command.get_direction()]))
        encoded_speed = struct.pack("f", command.get_speed().get_speed())
        self._serial.write(encoded_direction + encoded_speed)
        time.sleep(command.get_duration().get_duration())
