from math import pi
from typing import List

from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed


class MovementCommandFactory:
    def __init__(
        self,
        robot_maximum_speed: Speed,
        servoing_constant: Speed,
        base_command_duration: CommandDuration,
        rotating_speed: Speed,
        robot_radius: float,
    ):
        self._robot_maximum_speed = robot_maximum_speed
        self._servoing_constant = servoing_constant
        self._base_command_duration = base_command_duration
        self._rotating_speed = rotating_speed
        self._robot_radius = robot_radius

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

        movement_commands.append(self._create_stop_command())

        return movement_commands

    def create_from_angle(self, angle: float) -> List[MovementCommand]:
        duration = self._calculate_duration(angle)
        direction = Direction.CLOCKWISE if angle < 0 else Direction.COUNTER_CLOCKWISE

        rotating_command = MovementCommand(direction, self._rotating_speed, duration)
        return [rotating_command, self._create_stop_command()]

    def _create_stop_command(self):
        return MovementCommand(Direction.STOP, Speed(0), self._base_command_duration)

    def _calculate_duration(self, angle: float) -> CommandDuration:
        rotation_circle_arc = 2 * pi * self._robot_radius * angle / 360
        return CommandDuration(rotation_circle_arc / self._rotating_speed.get_speed())
