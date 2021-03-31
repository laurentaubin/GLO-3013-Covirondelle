import cv2

from config.config import WORLD_CAMERA_IMAGE_SIZE
from domain.camera.ICalibrator import ICalibrator
from domain.camera.IWorldCamera import IWorldCamera
from domain.camera.exception.InvalidCameraConfigException import (
    InvalidCameraConfigException,
)


class OpenCvWorldCamera(IWorldCamera):
    def __init__(self, camera_index: int, camera_calibrator: ICalibrator):
        self._camera_index = camera_index
        self._camera_calibrator = camera_calibrator
        self._capture = None
        self._open_capture()

    def take_world_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        if not opened_successfully:
            raise InvalidCameraConfigException
        return self._camera_calibrator.calibrate(current_frame)

    def _open_capture(self):
        self._capture = cv2.VideoCapture(self._camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, WORLD_CAMERA_IMAGE_SIZE[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, WORLD_CAMERA_IMAGE_SIZE[1])
        self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def _close_capture(self):
        self._capture.release()
