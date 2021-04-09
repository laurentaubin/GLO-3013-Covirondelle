from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.RotationCommand import RotationCommand
from domain.movement.Speed import Speed
from infra.motor_controller.StmMotorController import StmMotorController


@patch("serial.time.sleep", MagicMock())
class TestStmMotorController(TestCase):
    A_DIRECTION = Direction.FORWARD
    A_DISTANCE = Distance(distance=10)
    A_MOVEMENT = Movement(A_DIRECTION, A_DISTANCE)
    A_MOVEMENT_COMMAND = MovementCommand(
        Direction.LEFT, Speed(0.01), CommandDuration(0)
    )
    A_STOP_COMMAND = MovementCommand(Direction.STOP, Speed(0), CommandDuration(0.5))
    A_MOVEMENT_COMMAND_LIST = [
        MovementCommand(Direction.FORWARD, Speed(10), CommandDuration(10)),
        A_STOP_COMMAND,
    ]

    def setUp(self) -> None:
        self.serial_communication = MagicMock()
        self.stm_motor_controller = StmMotorController(self.serial_communication)

    def test_givenMultipleMovementCommands_whenActuateWheels_thenWriteOnSerialOncePerCommand(
        self,
    ):
        commands = self.A_MOVEMENT_COMMAND_LIST

        self.stm_motor_controller.actuate_wheels(commands)

        self.assertEqual(
            len(self.A_MOVEMENT_COMMAND_LIST),
            self.serial_communication.write.call_count,
        )

    def test_givenSingleMovementCommand_whenActuateWheels_thenSerializeCommandBeforeWritingOnSerial(
        self,
    ):
        a_direction = Direction.LEFT
        a_speed = Speed(0.147)
        commands = [MovementCommand(a_direction, a_speed, CommandDuration(100))]
        expected_serialization = b"\x03+\x87\x16>"

        self.stm_motor_controller.actuate_wheels(commands)

        self.serial_communication.write.assert_called_with(expected_serialization)

    def test_whenRotate_thenSerializeCommandBeforeWritingOnSerial(self):
        a_direction = Direction.CLOCKWISE
        an_angle = 15.4
        rotation_command = RotationCommand(a_direction, an_angle)
        expected_serialization = b"\x05ffvA"

        self.stm_motor_controller.rotate(rotation_command)

        self.serial_communication.write.assert_called_with(expected_serialization)

    def test_whenRotate_thenWaitForRobotResponse(self):
        a_direction = Direction.CLOCKWISE
        an_angle = 15.4
        rotation_command = RotationCommand(a_direction, an_angle)

        self.stm_motor_controller.rotate(rotation_command)

        self.serial_communication.readline.assert_called()
