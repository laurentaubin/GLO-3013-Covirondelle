import struct
from typing import List

from serial import Serial, time

from domain.IMotorController import IMotorController
from domain.movement.MovementCommand import MovementCommand
from domain.movement.RotationCommand import RotationCommand


class StmMotorController(IMotorController):
    def __init__(self, serial: Serial) -> None:
        self._serial = serial

    def actuate_wheels(self, commands: List[MovementCommand]) -> None:
        for command in commands:
            self._send_movement_command_to_motor(command)

    def rotate(self, command: RotationCommand) -> None:
        self._send_rotation_command_to_motor(command)

    def _send_movement_command_to_motor(self, command: MovementCommand):
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

    def _send_rotation_command_to_motor(self, command: RotationCommand) -> None:
        print(
            "Sending rotation command with direction %s and angle %f"
            % (
                command.get_direction().name,
                command.get_angle(),
            )
        )
        encoded_direction = bytes(([command.get_direction()]))
        encoded_speed = struct.pack("f", command.get_angle())
        self._serial.write(encoded_direction + encoded_speed)
        self._serial.readline()
