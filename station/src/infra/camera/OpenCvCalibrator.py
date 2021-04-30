import cv2
import numpy as np

# https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html
from domain.camera.ICalibrator import ICalibrator


class OpenCvCalibrator(ICalibrator):
    def __init__(self, calibration_file_path):
        calibration_matrix = np.load(calibration_file_path)
        self._camera_matrix = calibration_matrix["camera_matrix"]
        self._distortion_coefficients = calibration_matrix["distortion_coefficients"]

    def calibrate(self, image):
        height, width = image.shape[:2]
        new_camera_matrix, region_of_interest = cv2.getOptimalNewCameraMatrix(
            self._camera_matrix,
            self._distortion_coefficients,
            (width, height),
            1,
            (width, height),
        )
        undistorted_image = cv2.undistort(
            image,
            self._camera_matrix,
            self._distortion_coefficients,
            None,
            new_camera_matrix,
        )
        x, y, width, height = region_of_interest
        return undistorted_image

    def get_camera_matrix(self):
        return self._camera_matrix

    def get_distortion_coefficients(self):
        return self._distortion_coefficients
