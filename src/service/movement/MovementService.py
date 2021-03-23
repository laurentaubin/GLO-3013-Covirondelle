from domain.IMotorController import IMotorController
from domain.movement.MovementFactory import MovementFactory


class MovementService:
    def __init__(
        self,
        movement_command_factory: MovementFactory,
        motor_controller: IMotorController,
    ):
        self._movement_factory = movement_command_factory
        self._motor_controller = motor_controller

    def move(self, path):
        movements = self._movement_factory.create_movements(path)
        self._motor_controller.actuate_wheels(movements)
