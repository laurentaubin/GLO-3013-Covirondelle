from typing import List

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.RotationCommand import RotationCommand
from domain.movement.Speed import Speed


class MovementCommandFactory:
    def __init__(
        self,
        robot_maximum_speed: Speed,
        servoing_constant: Speed,
        base_command_duration: CommandDuration,
    ):
        self._robot_maximum_speed = robot_maximum_speed
        self._servoing_constant = servoing_constant
        self._base_command_duration = base_command_duration

    def create_from_movement(self, movement: Movement) -> List[MovementCommand]:
        distance_left = movement.get_distance().get_distance()

        movement_commands = list()
        while distance_left > 0.001:
            speed = min(
                self._robot_maximum_speed,
                Speed(self._servoing_constant * distance_left),
            )
            if speed * self._base_command_duration.get_duration() > distance_left:
                speed = Speed.calculate_from_distance_and_duration(
                    Distance(distance_left), self._base_command_duration
                )

            movement_command = MovementCommand(
                movement.get_direction(), speed, self._base_command_duration
            )
            movement_commands.append(movement_command)

            distance_left -= speed * self._base_command_duration.get_duration()

        movement_commands.append(self.create_stop_command())

        return movement_commands

    def create_from_angle(self, angle: float) -> RotationCommand:
        direction = Direction.CLOCKWISE if angle < 0 else Direction.COUNTER_CLOCKWISE

        rotating_command = RotationCommand(direction, abs(angle))
        return rotating_command

    def create_stop_command(self):
        return MovementCommand(Direction.STOP, Speed(0), self._base_command_duration)

    def create_alignment_movement_command(self, direction: Direction):
        return MovementCommand(
            direction, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )
