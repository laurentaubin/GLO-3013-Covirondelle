import time

import cv2

from config.config import CALIBRATION_FILE_PATH, LAPTOP_CAMERA_INDEX
from domain.Color import Color
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector

if __name__ == "__main__":
    calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
    camera = OpenCvWorldCamera(LAPTOP_CAMERA_INDEX, calibrator)
    detector = OpenCvPuckDetector()
    should_continue = True
    images = []

    while should_continue:
        image = camera.take_world_image()
        for color in Color:
            if color is Color.NONE:
                continue
            position = detector.detect(image, color)
            print("sucessfully detected color ", color.name)
            cv2.circle(
                image,
                position.to_tuple(),
                25,
                (0, 255, 0),
                1,
            )
            text_position = (
                position.get_x_coordinate() - 20,
                position.get_y_coordinate() - 16,
            )
            cv2.putText(
                image,
                color.name,
                text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                20,
            )

        cv2.imshow("image", image)
        k = cv2.waitKey(1)
        if k == 27:  # Esc key to stop
            break
