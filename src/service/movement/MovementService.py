from domain.IMotorController import IMotorController
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.MovementFactory import MovementFactory


class MovementService:
    def __init__(
        self,
        movement_factory: MovementFactory,
        movement_command_factory: MovementCommandFactory,
        motor_controller: IMotorController,
    ):
        self._movement_factory = movement_factory
        self._movement_command_factory = movement_command_factory
        self._motor_controller = motor_controller

    def move(self, path):
        movements = self._movement_factory.create_movements(path)
        movement_commands = list()

        for movement in movements:
            movement_commands += (
                self._movement_command_factory.generate_commands_from_movement(movement)
            )

        self._motor_controller.actuate_wheels(movement_commands)
