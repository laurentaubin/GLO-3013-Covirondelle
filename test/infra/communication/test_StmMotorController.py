from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from infra.communication.motor_controller.StmMotorController import StmMotorController


@patch("serial.time.sleep", MagicMock())
class TestStmMotorController(TestCase):
    A_DIRECTION = Direction.FORWARD
    A_DISTANCE = Distance(distance=10)
    A_MOVEMENT = Movement(A_DIRECTION, A_DISTANCE)
    A_STOP_COMMAND = MovementCommand(Direction.STOP, Speed(0), CommandDuration(0.5))
    A_MOVEMENT_COMMAND_LIST = [
        MovementCommand(Direction.FORWARD, Speed(10), CommandDuration(10)),
        A_STOP_COMMAND,
    ]

    def setUp(self) -> None:
        self.serial_communication = MagicMock()
        self.movement_command_factory = MagicMock()
        self.stm_motor_controller = StmMotorController(
            self.serial_communication, self.movement_command_factory
        )

    def test_whenActuateWheels_thenSerialCommunicationIsUsedToTalkToStm(self):
        self.movement_command_factory.generate_commands_from_movement.return_value = (
            self.A_MOVEMENT_COMMAND_LIST
        )
        movements = [self.A_MOVEMENT]

        self.stm_motor_controller.actuate_wheels(movements)

        self.serial_communication.write.assert_called()
