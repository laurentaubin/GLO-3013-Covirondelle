# https://pypi.org/project/imagezmq/

import socket
from unittest.mock import MagicMock

import cv2
import imagezmq

from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera
from infra.vision.OpenCvCornerDetector import OpenCvCornerDetector
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector
from infra.vision.OpenCvStartingZoneLineDetector import OpenCvStartingZoneLineDetector
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)

if __name__ == "__main__":
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 500)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    sender = imagezmq.ImageSender(connect_to="tcp://10.240.113.37:5557")
    puck_detector = OpenCvPuckDetector()
    command_panel_letters_extractor = PytesseractLetterPositionExtractor()
    corner_detector = OpenCvCornerDetector()
    line_detector = OpenCvStartingZoneLineDetector()
    camera = OpenCvEmbeddedCamera(
        0, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )
    rpi_name = socket.gethostname()

    while True:
        image = camera.take_image()
        try:
            # letters = command_panel_letters_extractor.extract_letters_from_image(
            #     image
            # )
            position = line_detector.detect(image)
            cv2.circle(
                image,
                (
                    int(position.get_x_coordinate()),
                    int(position.get_y_coordinate()),
                ),
                20,
                (0, 255, 0),
                2,
            )
            print(position)
        except Exception:
            print("not found")
            pass
        print("sending")
        sender.send_image(rpi_name, image)
