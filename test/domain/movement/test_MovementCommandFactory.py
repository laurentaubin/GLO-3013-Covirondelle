from unittest import TestCase

from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed


class TestMovementCommandFactory(TestCase):
    AN_ALIGNMENT_SPEED = Speed(0.01)
    A_ROBOT_MAXIMUM_SPEED = Speed(0.25)
    A_SEVOING_CONSTANT = Speed(5)
    A_COMMAND_DURATION = CommandDuration(0.1)
    A_DIRECTION = Direction.LEFT
    A_DISTANCE = Distance(1)

    def setUp(self) -> None:
        self.movement_command_factory = MovementCommandFactory(
            self.A_ROBOT_MAXIMUM_SPEED,
            self.A_SEVOING_CONSTANT,
            self.A_COMMAND_DURATION,
        )

    def test_whenGenerateCommandsFromMovement_thenLastCommandHasStopDirection(self):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(a_movement)
        )
        last_movement_command = movement_commands[-1]

        self.assertEqual(Direction.STOP, last_movement_command.get_direction())

    def test_givenMovementGoingForward_whenGenerateCommandsFromMovement_thenAllCommandsExceptLastHaveForwardDirection(
        self,
    ):
        a_movement = Movement(Direction.FORWARD, self.A_DISTANCE)
        expected_directions = {Direction.FORWARD}

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(a_movement)
        )

        actual_directions = {
            command.get_direction() for command in movement_commands[:-1]
        }
        self.assertEqual(expected_directions, actual_directions)

    def test_givenMovementGoingBackwards_whenGenerateCommandsFromMovement_thenAllCommandsExceptLastHaveBackwardsDirection(
        self,
    ):
        a_movement = Movement(Direction.BACKWARDS, self.A_DISTANCE)
        expected_directions = {Direction.BACKWARDS}

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(a_movement)
        )

        actual_directions = {
            command.get_direction() for command in movement_commands[:-1]
        }
        self.assertEqual(expected_directions, actual_directions)

    def test_givenLongMovement_whenGenerateCommandsFromMovement_thenFirstCommandsUseMaximumRobotSpeed(
        self,
    ):
        a_long_movement = Movement(self.A_DIRECTION, Distance(1000))

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(
                a_long_movement
            )
        )
        first_movement, second_movement, *_ = movement_commands

        self.assertEqual(self.A_ROBOT_MAXIMUM_SPEED, first_movement.get_speed())
        self.assertEqual(self.A_ROBOT_MAXIMUM_SPEED, second_movement.get_speed())

    def test_whenGenerateCommandsFromMovement_thenLastCommandsHaveSpeedLessThanMaximumRobotSpeed(
        self,
    ):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(a_movement)
        )
        last_non_stop_command = movement_commands[-2]

        self.assertLess(
            last_non_stop_command.get_speed(),
            self.A_ROBOT_MAXIMUM_SPEED,
        )

    def test_givenASetCommandDuration_whenGenerateCommandsFromMovement_thenAllCommandsHaveThisDuration(
        self,
    ):
        a_movement = Movement(self.A_DIRECTION, self.A_DISTANCE)
        expected_durations = {self.A_COMMAND_DURATION}

        movement_commands = (
            self.movement_command_factory.generate_commands_from_movement(a_movement)
        )

        actual_durations = {command.get_duration() for command in movement_commands}
        self.assertEqual(expected_durations, actual_durations)
