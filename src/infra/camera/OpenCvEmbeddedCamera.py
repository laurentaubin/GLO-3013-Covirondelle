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
        self._maestro_controller = maestro_controller
        self._horizontal_servo_id = horizontal_servo_id
        self._vertical_servo_id = vertical_servo_id
        self._horizontal_angle_range = horizontal_angle_range
        self._vertical_angle_range = vertical_angle_range

        self._capture = self._open_capture()

        self._buffer_size = int(self._capture.get(cv2.CAP_PROP_BUFFERSIZE))

    def rotate_horizontally(self, target: int) -> None:
        self._maestro_controller.setTarget(self._horizontal_servo_id, target)

    def rotate_vertically(self, target: int) -> None:
        self._maestro_controller.setTarget(self._vertical_servo_id, target)

    def take_image(self):
        self._clear_buffer()
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        if not opened_successfully:
            raise InvalidCameraException
        return current_frame

    def _open_capture(self):
        capture = cv2.VideoCapture(self._camera_index)
        capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        capture.set(cv2.CAP_PROP_CONTRAST, 20)
        capture.set(cv2.CAP_PROP_SATURATION, 30)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, EMBEDDED_CAMERA_IMAGE_SIZE[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, EMBEDDED_CAMERA_IMAGE_SIZE[1])
        return capture

    def _close_capture(self):
        self._capture.release()

    def _clear_buffer(self):
        for i in range(self._buffer_size):
            self._capture.grab()
