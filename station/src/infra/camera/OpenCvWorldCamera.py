import queue
import threading

import cv2

from config.config import WORLD_CAMERA_IMAGE_SIZE
from domain.camera.ICalibrator import ICalibrator
from domain.camera.IWorldCamera import IWorldCamera


class OpenCvWorldCamera(IWorldCamera):
    def __init__(self, camera_index: int, camera_calibrator: ICalibrator):
        self._camera_index = camera_index
        self._camera_calibrator = camera_calibrator
        self._capture = self._open_capture()
        self._buffer_size = int(self._capture.get(cv2.CAP_PROP_BUFFERSIZE))

    def take_world_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        self._clear_buffer()
        ret, current_frame = self._capture.read()
        return self._camera_calibrator.calibrate(current_frame)

    def _clear_buffer(self):
        for i in range(self._buffer_size):
            self._capture.grab()

    def _open_capture(self):
        capture = cv2.VideoCapture(self._camera_index, cv2.CAP_V4L2)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        capture.set(cv2.CAP_PROP_FOCUS, 1)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, WORLD_CAMERA_IMAGE_SIZE[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, WORLD_CAMERA_IMAGE_SIZE[1])
        capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        capture.set(cv2.CAP_PROP_CONTRAST, 22)
        capture.set(cv2.CAP_PROP_SATURATION, 30)
        return capture

    def _close_capture(self):
        self._capture.release()
