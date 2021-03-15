from typing import List

from domain.communication.IMotorController import IMotorController
from domain.movement.Movement import Movement


class FakeMotorController(IMotorController):
    def actuate_wheels(self, command: List[Movement]) -> None:
        pass
