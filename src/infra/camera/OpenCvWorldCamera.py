import cv2

from domain.camera.IWorldCamera import IWorldCamera
from domain.camera.exception.InvalidCameraConfigException import (
    InvalidCameraConfigException,
)


class OpenCvWorldCamera(IWorldCamera):
    def __init__(self, camera_index: int):
        self._camera_index = camera_index
        self._capture = None
        self._open_capture()

    def take_world_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        if not opened_successfully:
            raise InvalidCameraConfigException
        return current_frame

    def _open_capture(self):
        self._capture = cv2.VideoCapture(self._camera_index)

    def _close_capture(self):
        self._capture.release()
