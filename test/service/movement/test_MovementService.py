from unittest import TestCase
from unittest.mock import MagicMock

from service.movement.MovementService import MovementService


class TestMovementService(TestCase):
    A_MOVEMENT = MagicMock()
    ANOTHER_MOVEMENT = MagicMock()
    A_COMMAND = MagicMock()
    AN_ANGLE = 123.4
    A_MOVEMENT_COMMAND = MagicMock()

    def setUp(self) -> None:
        self.movement_command_factory = MagicMock()
        self.motor_controller = MagicMock()
        self.movement_service = MovementService(
            self.movement_command_factory, self.motor_controller
        )

    def test_givenMovements_whenMove_thenUseMovementCommandFactoryToCreateCommands(
        self,
    ):
        self.movement_service.move(
            [
                self.A_MOVEMENT,
                self.ANOTHER_MOVEMENT,
            ]
        )

        self.movement_command_factory.generate_commands_from_movement.has_any_call(
            self.A_MOVEMENT
        )
        self.movement_command_factory.generate_commands_from_movement.has_any_call(
            self.ANOTHER_MOVEMENT
        )

    def test_whenMove_thenUseMotorControllerToSendCommandsToWheels(self):
        self.movement_command_factory.create_from_movement.return_value = [
            self.A_COMMAND
        ]

        self.movement_service.move([self.A_MOVEMENT])

        self.motor_controller.actuate_wheels.assert_called_with([self.A_COMMAND])

    def test_whenRotate_thenCreateMovementCommands(self):
        an_angle = 12.2

        self.movement_service.rotate(an_angle)

        self.movement_command_factory.create_from_angle.assert_called_with(an_angle)

    def test_givenRotationMovementCommand_whenRotate_thenUseMotorControllerToSendCommandsToWheels(
        self,
    ):
        self.movement_command_factory.create_from_angle.return_value = self.A_COMMAND

        self.movement_service.rotate(self.AN_ANGLE)

        self.motor_controller.rotate.assert_called_with(self.A_COMMAND)

    def test_whenExecuteCommandMovement_thenUseMotorControllerToSendCommandToTheWheels(
        self,
    ):
        self.movement_service.execute_movement_command(self.A_MOVEMENT_COMMAND)

        self.motor_controller.actuate_wheels.assert_called_with(
            [self.A_MOVEMENT_COMMAND]
        )
