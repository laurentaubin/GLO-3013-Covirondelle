import struct
from typing import List

from serial import Serial, time

from domain.IMotorController import IMotorController
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.MovementCommandFactory import MovementCommandFactory


class StmMotorController(IMotorController):
    def __init__(
        self, serial: Serial, movement_command_factory: MovementCommandFactory
    ) -> None:
        self._serial = serial
        self._movement_command_factory = movement_command_factory

    def actuate_wheels(self, movements: List[Movement]) -> None:

        commands = list()
        for movement in movements:
            commands += self._movement_command_factory.generate_commands_from_movement(
                movement
            )

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

        encoded_direction = bytes(chr(command.get_direction()), "utf-8")
        encoded_speed = struct.pack("f", command.get_speed().get_speed())
        self._serial.write(encoded_direction + encoded_speed)
        time.sleep(command.get_duration().get_duration())

        print("Response from STM32: %s" % self._serial.readline().decode("utf-8"))
