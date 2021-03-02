import cv2

from src.domain.vision.camera.CameraConfig import CameraConfig
from src.domain.vision.camera.exception.InvalidCameraConfigException import (
    InvalidCameraConfigException,
)


class WorldCamera:
    def __init__(self, camera_index: CameraConfig):
        self.camera_index = camera_index
        self.capture = None
        self.open_capture()

    def get_current_image_rgb(self):
        return self._get_camera_frame()

    def get_current_image_grayscale(self):
        gray_img = cv2.cvtColor(self._get_camera_frame(), cv2.COLOR_BGR2GRAY)
        return gray_img

    def _get_camera_frame(self):
        opened_successfully, current_frame = self.capture.read()

        if not opened_successfully:
            raise InvalidCameraConfigException

        return current_frame

    def open_capture(self):
        self.capture = cv2.VideoCapture(self.camera_index)

    def close_capture(self):
        self.capture.release()
