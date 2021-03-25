from unittest import TestCase
from unittest.mock import MagicMock

from service.movement.MovementService import MovementService


class TestMovementService(TestCase):
    A_PATH = MagicMock()
    A_MOVEMENT = MagicMock()
    ANOTHER_MOVEMENT = MagicMock()
    A_COMMAND = MagicMock()

    def setUp(self) -> None:
        self.movement_factory = MagicMock()
        self.movement_command_factory = MagicMock()
        self.motor_controller = MagicMock()
        self.movement_service = MovementService(
            self.movement_factory, self.movement_command_factory, self.motor_controller
        )

    def test_whenMove_thenUseMovementFactoryToCreateMovements(self):
        self.movement_service.move(self.A_PATH)

        self.movement_factory.create_movements.assert_called_with(self.A_PATH)

    def test_givenMovements_whenMove_thenUseMovementCommandFactoryToCreateCommands(
        self,
    ):
        self.movement_factory.create_movements.return_value = [
            self.A_MOVEMENT,
            self.ANOTHER_MOVEMENT,
        ]

        self.movement_service.move(self.A_PATH)

        self.movement_command_factory.generate_commands_from_movement.has_any_call(
            self.A_MOVEMENT
        )
        self.movement_command_factory.generate_commands_from_movement.has_any_call(
            self.ANOTHER_MOVEMENT
        )

    def test_whenMove_thenUseMotorControllerToSendCommandsToWheels(self):
        self.movement_factory.create_movements.return_value = [self.A_MOVEMENT]
        self.movement_command_factory.generate_commands_from_movement.return_value = [
            self.A_COMMAND
        ]

        self.movement_service.move(self.A_PATH)

        self.motor_controller.actuate_wheels.assert_called_with([self.A_COMMAND])
