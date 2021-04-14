from typing import List

from domain.Orientation import Orientation
from domain.Position import Position
from domain.exception.InvalidOrientationException import InvalidOrientationException
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.pathfinding.Path import Path
from infra.utils.GeometryUtils import GeometryUtils


class MovementFactory:
    def __init__(self):
        self._direction_to_orientation = {
            Direction.LEFT: Orientation(90),
            Direction.RIGHT: Orientation(270),
            Direction.FORWARD: Orientation(0),
            Direction.BACKWARDS: Orientation(180),
        }
        self._orientation_to_direction = {
            88: Direction.LEFT,
            89: Direction.LEFT,
            90: Direction.LEFT,
            91: Direction.LEFT,
            92: Direction.LEFT,
            268: Direction.RIGHT,
            269: Direction.RIGHT,
            270: Direction.RIGHT,
            271: Direction.RIGHT,
            272: Direction.RIGHT,
            358: Direction.FORWARD,
            359: Direction.FORWARD,
            0: Direction.FORWARD,
            1: Direction.FORWARD,
            2: Direction.FORWARD,
            178: Direction.BACKWARDS,
            179: Direction.BACKWARDS,
            180: Direction.BACKWARDS,
            181: Direction.BACKWARDS,
            182: Direction.BACKWARDS,
        }

    def create_movements(
        self, original_path: Path, orientation: Orientation
    ) -> List[Movement]:
        sub_paths = self._split_path_in_sub_paths(original_path)

        movements = list()
        for path in sub_paths:
            movements.append(
                self._create_movement_from_straight_path(path, orientation)
            )

        return movements

    def _split_path_in_sub_paths(self, full_path: Path) -> List[Path]:
        sub_paths = list()

        if not self._path_has_turn(full_path):
            sub_paths.append(full_path)
            return sub_paths

        current_position = 1
        path_length = len(full_path) + 1
        current_path = Path([])
        while current_position < path_length:
            is_current_direction_vertical = self._are_positions_moving_vertically(
                full_path[current_position - 1], full_path[current_position]
            )
            if is_current_direction_vertical:
                while is_current_direction_vertical and current_position < path_length:
                    current_path.add(full_path[current_position - 1])
                    is_current_direction_vertical = self._is_current_direction_vertical(
                        is_current_direction_vertical,
                        current_position,
                        path_length,
                        full_path,
                    )
                    current_position += 1
            else:
                while (
                    not is_current_direction_vertical and current_position < path_length
                ):
                    current_path.add(full_path[current_position - 1])
                    is_current_direction_vertical = self._is_current_direction_vertical(
                        is_current_direction_vertical,
                        current_position,
                        path_length,
                        full_path,
                    )
                    current_position += 1

            sub_paths.append(current_path)
            current_path = Path([])

        return sub_paths

    def _path_has_turn(self, path: Path) -> bool:
        if self._are_positions_moving_horizontally(path[0], path[1]) > 0:
            for i in range(1, len(path)):
                if self._are_positions_moving_vertically(path[i - 1], path[i]) > 0:
                    return True
        else:
            for i in range(1, len(path)):
                if self._are_positions_moving_horizontally(path[i - 1], path[i]) > 0:
                    return True
        return False

    def _are_positions_moving_horizontally(
        self, first_position: Position, second_position: Position
    ) -> bool:
        return (
            abs(first_position.get_x_coordinate() - second_position.get_x_coordinate())
            == 1
        )

    def _are_positions_moving_vertically(
        self, first_position: Position, second_position: Position
    ) -> bool:
        return (
            abs(first_position.get_y_coordinate() - second_position.get_y_coordinate())
            == 1
        )

    def _is_current_direction_vertical(
        self,
        is_current_direction_vertical: bool,
        current_position: int,
        path_length: int,
        full_path: Path,
    ) -> bool:
        if current_position == path_length - 1:
            return not is_current_direction_vertical

        return self._are_positions_moving_vertically(
            full_path[current_position - 1],
            full_path[current_position],
        )

    def _create_movement_from_straight_path(
        self, path: Path, orientation: Orientation
    ) -> Movement:
        direction = None
        if path[1].get_x_coordinate() - path[0].get_x_coordinate() == 1:
            direction = self._calculate_movement_from_orientation(
                orientation, Direction.FORWARD
            )
        elif path[1].get_x_coordinate() - path[0].get_x_coordinate() == -1:
            direction = self._calculate_movement_from_orientation(
                orientation, Direction.BACKWARDS
            )
        elif path[1].get_y_coordinate() - path[0].get_y_coordinate() == 1:
            direction = self._calculate_movement_from_orientation(
                orientation, Direction.RIGHT
            )
        elif path[1].get_y_coordinate() - path[0].get_y_coordinate() == -1:
            direction = self._calculate_movement_from_orientation(
                orientation, Direction.LEFT
            )
        return Movement(direction, Distance(len(path)))

    def _calculate_movement_from_orientation(
        self, current_orientation: Orientation, absolute_direction: Direction
    ) -> Direction:
        absolute_orientation = self._find_orientation_from_direction(absolute_direction)
        orientation_offset = absolute_orientation - current_orientation
        return self._find_direction_from_orientation(orientation_offset)

    def _find_orientation_from_direction(self, direction: Direction) -> Orientation:
        return self._direction_to_orientation.get(direction)

    def _find_direction_from_orientation(self, orientation: Orientation) -> Direction:
        if orientation.get_orientation_in_degree() < 0:
            orientation = Orientation(360 + orientation.get_orientation_in_degree())

        direction = self._orientation_to_direction.get(
            orientation.get_orientation_in_degree()
        )

        if direction is None:
            raise InvalidOrientationException
        return direction

    def create_movement_to_get_to_point_with_direction(
        self, first_position, second_position, direction
    ):
        distance = GeometryUtils.calculate_distance_between_two_positions(
            first_position, second_position
        )

        return Movement(direction, distance)
