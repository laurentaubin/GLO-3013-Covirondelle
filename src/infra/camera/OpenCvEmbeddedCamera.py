import cv2

from domain.camera.IEmbeddedCamera import IEmbeddedCamera
from domain.camera.exception.InvalidCameraException import InvalidCameraException
from config.config import EMBEDDED_CAMERA_IMAGE_SIZE


class OpenCvEmbeddedCamera(IEmbeddedCamera):
    def __init__(self, camera_index: int):
        self._camera_index = camera_index
        self._capture = None
        self._open_capture()

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
