from unittest import TestCase
from unittest.mock import MagicMock

from service.movement.MovementService import MovementService


class TestMovementService(TestCase):
    A_PATH = MagicMock()

    def setUp(self) -> None:
        self.movement_factory = MagicMock()
        self.motor_controller = MagicMock()
        self.movement_service = MovementService(
            self.movement_factory, self.motor_controller
        )

    def test_whenMove_thenUseMovementFactoryToCreateMovements(self):
        self.movement_service.move(self.A_PATH)

        self.movement_factory.create_movements.assert_called_with(self.A_PATH)

    def test_whenMove_thenUseMotorControllerToSendCommandsToWheels(self):
        self.movement_service.move(self.A_PATH)

        self.motor_controller.actuate_wheels.assert_called()
