from typing import List

from domain.movement.Movement import Movement


class IMotorController:
    def actuate_wheels(self, command: List[Movement]) -> None:
        pass
