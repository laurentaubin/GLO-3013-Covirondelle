from typing import Tuple

import cv2

from domain.camera.IEmbeddedCamera import IEmbeddedCamera
from domain.camera.exception.InvalidCameraException import InvalidCameraException
from config.config import EMBEDDED_CAMERA_IMAGE_SIZE
from infra.MaestroController import MaestroController


class OpenCvEmbeddedCamera(IEmbeddedCamera):
    def __init__(
        self,
        camera_index: int,
        maestro_controller: MaestroController,
        horizontal_servo_id: int,
        vertical_servo_id: int,
        horizontal_angle_range: Tuple[float, float],
        vertical_angle_range: Tuple[float, float],
    ):
        self._camera_index = camera_index
        self._capture = None
        self._maestro_controller = maestro_controller
        self._horizontal_servo_id = horizontal_servo_id
        self._vertical_servo_id = vertical_servo_id
        self._horizontal_angle_range = horizontal_angle_range
        self._vertical_angle_range = vertical_angle_range

        self._open_capture()

    def rotate_horizontally(self, angle: float) -> None:
        target = self._find_target_from_angle_range(angle, self._horizontal_angle_range)

        self._maestro_controller.setTarget(self._horizontal_servo_id, target)

    def rotate_vertically(self, angle: float) -> None:
        target = self._find_target_from_angle_range(angle, self._vertical_angle_range)

        self._maestro_controller.setTarget(self._vertical_servo_id, target)

    def take_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        if not opened_successfully:
            raise InvalidCameraException
        return current_frame

    def _open_capture(self):
        self._capture = cv2.VideoCapture(self._camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, EMBEDDED_CAMERA_IMAGE_SIZE[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, EMBEDDED_CAMERA_IMAGE_SIZE[1])

    def _close_capture(self):
        self._capture.release()

    def _find_target_from_angle_range(self, angle, angle_range):
        minimum_angle, maximum_angle = angle_range
        return angle / 360 * (maximum_angle - minimum_angle) + minimum_angle
