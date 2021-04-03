from unittest import TestCase

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed


class TestMovementCommandFactory(TestCase):
    AN_ALIGNMENT_SPEED = Speed(0.01)
    A_ROBOT_MAXIMUM_SPEED = Speed(0.25)
    A_SEVOING_CONSTANT = Speed(5)
    A_COMMAND_DURATION = CommandDuration(0.1)
    A_DIRECTION = Direction.LEFT
    A_DISTANCE = Distance(1)
    AN_ANGLE = 43.1
    ROTATING_SPEED = Speed(0.2)
    ROBOT_RADIUS = 0.1075
    SLOW_MOVEMENT_SPEED = Speed(ROBOT_ALIGNMENT_SPEED)
    CONTINUOUS_MOVEMENT_DURATION = CommandDuration(0)
    NULL_SPEED = Speed(0)
    NULL_COMMAND_DURATION = CommandDuration(0)

    def setUp(self) -> None:
        self.movement_command_factory = MovementCommandFactory(
            self.A_ROBOT_MAXIMUM_SPEED,
            self.A_SEVOING_CONSTANT,
            self.A_COMMAND_DURATION,
            self.ROTATING_SPEED,
            self.ROBOT_RADIUS,
        )

    def test_whenCreateFromMovement_thenLastCommandHasStopDirection(self):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)

        movement_commands = self.movement_command_factory.create_from_movement(
            a_movement
        )
        last_movement_command = movement_commands[-1]

        self.assertEqual(Direction.STOP, last_movement_command.get_direction())

    def test_givenMovementGoingForward_whenCreateFromMovement_thenAllCommandsExceptLastHaveForwardDirection(
        self,
    ):
        a_movement = Movement(Direction.FORWARD, self.A_DISTANCE)
        expected_directions = {Direction.FORWARD}

        movement_commands = self.movement_command_factory.create_from_movement(
            a_movement
        )

        actual_directions = {
            command.get_direction() for command in movement_commands[:-1]
        }
        self.assertEqual(expected_directions, actual_directions)

    def test_givenMovementGoingBackwards_whenCreateFromMovement_thenAllCommandsExceptLastHaveBackwardsDirection(
        self,
    ):
        a_movement = Movement(Direction.BACKWARDS, self.A_DISTANCE)
        expected_directions = {Direction.BACKWARDS}

        movement_commands = self.movement_command_factory.create_from_movement(
            a_movement
        )

        actual_directions = {
            command.get_direction() for command in movement_commands[:-1]
        }
        self.assertEqual(expected_directions, actual_directions)

    def test_givenLongMovement_whenCreateFromMovement_thenFirstCommandsUseMaximumRobotSpeed(
        self,
    ):
        a_long_movement = Movement(self.A_DIRECTION, Distance(1000))

        movement_commands = self.movement_command_factory.create_from_movement(
            a_long_movement
        )
        first_movement, second_movement, *_ = movement_commands

        self.assertEqual(self.A_ROBOT_MAXIMUM_SPEED, first_movement.get_speed())
        self.assertEqual(self.A_ROBOT_MAXIMUM_SPEED, second_movement.get_speed())

    def test_whenCreateFromMovement_thenLastCommandsHaveSpeedLessThanMaximumRobotSpeed(
        self,
    ):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)

        movement_commands = self.movement_command_factory.create_from_movement(
            a_movement
        )
        last_non_stop_command = movement_commands[-2]

        self.assertLess(
            last_non_stop_command.get_speed(),
            self.A_ROBOT_MAXIMUM_SPEED,
        )

    def test_givenASetCommandDuration_whenCreateFromMovement_thenAllCommandsHaveThisDuration(
        self,
    ):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)
        expected_durations = {self.A_COMMAND_DURATION}

        movement_commands = self.movement_command_factory.create_from_movement(
            a_movement
        )

        actual_durations = {command.get_duration() for command in movement_commands}
        self.assertEqual(expected_durations, actual_durations)

    def test_givenAPositiveAngle_whenCreateFromAngle_thenReturnCommandWithCounterClockwiseDirection(
        self,
    ):
        a_positive_angle = 12.3

        actual_command = self.movement_command_factory.create_from_angle(
            a_positive_angle
        )[0]

        self.assertEqual(Direction.COUNTER_CLOCKWISE, actual_command.get_direction())

    def test_givenANegativeAngle_whenCreateFromAngle_thenReturnCommandWithClockwiseDirection(
        self,
    ):
        a_negative_angle = -12.3

        actual_command = self.movement_command_factory.create_from_angle(
            a_negative_angle
        )[0]

        self.assertEqual(Direction.CLOCKWISE, actual_command.get_direction())

    def test_whenCreateFromAngle_thenReturnCommandWithRotationSpeed(self):
        actual_command = self.movement_command_factory.create_from_angle(self.AN_ANGLE)[
            0
        ]

        self.assertEqual(self.ROTATING_SPEED, actual_command.get_speed())

    def test_whenCreateFromAngle_thenLastCommandIsAStopCommand(self):
        commands = self.movement_command_factory.create_from_angle(self.AN_ANGLE)
        last_command = commands[-1]

        self.assertEqual(Direction.STOP, last_command.get_direction())

    def test_givenRobotRadius_whenCreateFromAngle_thenCalculateRotationDurationAndSetDurationToCommand(
        self,
    ):
        expected_duration = CommandDuration(0.4043)

        rotation_command = self.movement_command_factory.create_from_angle(
            self.AN_ANGLE
        )[0]

        self.assertEqual(expected_duration, rotation_command.get_duration())

    def test_givenBackwardsDirection_whenCreateAlignmentMovementCommand_thenSlowContinuousBackwardsMovementCommandIsCreated(
        self,
    ):
        expected_movement_command = MovementCommand(
            Direction.BACKWARDS,
            self.SLOW_MOVEMENT_SPEED,
            self.CONTINUOUS_MOVEMENT_DURATION,
        )

        actual_movement_command = (
            self.movement_command_factory.create_alignment_movement_command(
                Direction.BACKWARDS
            )
        )

        self.assertEqual(actual_movement_command, expected_movement_command)

    def test_whenCreateStopMovementCommand_thenStopMovementCommandIsCreated(self):
        expected_movement_command = MovementCommand(
            Direction.STOP, self.NULL_SPEED, self.A_COMMAND_DURATION
        )

        actual_movement_command = self.movement_command_factory.create_stop_command()

        self.assertEqual(actual_movement_command, expected_movement_command)
