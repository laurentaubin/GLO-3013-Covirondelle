from typing import List

from domain.Position import Position
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.pathfinding.Path import Path


class MovementFactory:
    def create_movements(self, original_path: Path) -> List[Movement]:
        sub_paths = self._split_path_in_sub_paths(original_path)

        movements = list()
        for path in sub_paths:
            movements.append(self._create_movement_from_straight_path(path))

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

    def _create_movement_from_straight_path(self, path: Path) -> Movement:
        if path[1].get_x_coordinate() - path[0].get_x_coordinate() == 1:
            return Movement(Direction.FORWARD, Distance(distance=len(path)))
        if path[1].get_x_coordinate() - path[0].get_x_coordinate() == -1:
            return Movement(Direction.BACKWARDS, Distance(distance=len(path)))
        if path[1].get_y_coordinate() - path[0].get_y_coordinate() == 1:
            return Movement(Direction.RIGHT, Distance(distance=len(path)))
        if path[1].get_y_coordinate() - path[0].get_y_coordinate() == -1:
            return Movement(Direction.LEFT, Distance(distance=len(path)))

        # will never happen
        raise Exception

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
