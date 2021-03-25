from typing import List

from domain.movement.MovementCommand import MovementCommand


class IMotorController:
    def actuate_wheels(self, command: List[MovementCommand]) -> None:
        pass
