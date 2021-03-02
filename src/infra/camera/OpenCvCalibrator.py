import cv2
import numpy as np

# https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html
from domain.camera.ICalibrator import ICalibrator


class OpenCvCalibrator(ICalibrator):
    def __init__(self, calibration_file_path):
        calibration_matrix = np.load(calibration_file_path)
        self.camera_matrix = calibration_matrix["camera_matrix"]
        self.distortion_coefficients = calibration_matrix["distortion_coefficients"]

    def calibrate(self, image):
        h, w = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix, self.distortion_coefficients, (w, h), 1, (w, h)
        )
        undistorted_image = cv2.undistort(
            image,
            self.camera_matrix,
            self.distortion_coefficients,
            None,
            new_camera_matrix,
        )
        x, y, w, h = roi
        undistorted_image = undistorted_image[y : y + h, x : x + w]
        return undistorted_image


if __name__ == "__main__":
    calibrator = OpenCvCalibrator("../../config/numpy.npz")
    image = cv2.imread("chessboard.jpg")
    calibrated_image = calibrator.calibrate(image)
    cv2.imshow("original", image)
    cv2.imshow("calibrated", calibrated_image)
    cv2.waitKey(0)
