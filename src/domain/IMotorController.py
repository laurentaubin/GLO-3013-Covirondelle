from typing import List

from domain.movement.MovementCommand import MovementCommand
from domain.movement.RotationCommand import RotationCommand


class IMotorController:
    def actuate_wheels(self, commands: List[MovementCommand]) -> None:
        pass

    def rotate(self, command: RotationCommand) -> None:
        pass
