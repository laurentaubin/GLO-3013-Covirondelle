from typing import List

from domain.IMotorController import IMotorController
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Movement import Movement
from domain.movement.MovementCommandFactory import MovementCommandFactory


class MovementService:
    def __init__(
        self,
        movement_command_factory: MovementCommandFactory,
        motor_controller: IMotorController,
    ):
        self._movement_command_factory = movement_command_factory
        self._motor_controller = motor_controller

    def move(self, movements: List[Movement]):
        movement_commands = list()

        for movement in movements:
            movement_commands += self._movement_command_factory.create_from_movement(
                movement
            )

        self._motor_controller.actuate_wheels(movement_commands)

    def rotate(self, angle: float):
        rotation_commands = self._movement_command_factory.create_from_angle(angle)
        self._motor_controller.rotate(rotation_commands)

    def execute_movement_command(self, movement_command: MovementCommand):
        self._motor_controller.actuate_wheels([movement_command])
