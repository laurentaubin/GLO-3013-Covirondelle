from typing import Tuple

from domain.communication.IEmbeddedCamera import IEmbeddedCamera
from infra.communication.camera import MaestroController


class MaestroEmbeddedCamera(IEmbeddedCamera):
    def __init__(
        self,
        maestro_controller: MaestroController,
        horizontal_servo_id: int,
        vertical_servo_id: int,
        horizontal_angle_range: Tuple[float, float],
        vertical_angle_range: Tuple[float, float],
    ):
        self._maestro_controller = maestro_controller
        self._horizontal_servo_id = horizontal_servo_id
        self._vertical_servo_id = vertical_servo_id
        self._horizontal_angle_range = horizontal_angle_range
        self._vertical_angle_range = vertical_angle_range

    def rotate_horizontally(self, angle: float) -> None:
        target = self._find_target_from_angle_range(angle, self._horizontal_angle_range)

        self._maestro_controller.setTarget(self._horizontal_servo_id, target)

    def rotate_vertically(self, angle: float) -> None:
        target = self._find_target_from_angle_range(angle, self._vertical_angle_range)

        self._maestro_controller.setTarget(self._vertical_servo_id, target)

    def _find_target_from_angle_range(self, angle, angle_range):
        minimum_angle, maximum_angle = angle_range
        return angle / 360 * (maximum_angle - minimum_angle) + minimum_angle
