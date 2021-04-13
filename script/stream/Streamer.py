# https://pypi.org/project/imagezmq/

import socket
import time
import cv2
import imagezmq

from domain.Color import Color
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector

if __name__ == "__main__":
    sender = imagezmq.ImageSender(connect_to="tcp://10.240.26.77:5557")
    puck_detector = OpenCvPuckDetector()

    rpi_name = socket.gethostname()
    capture = cv2.VideoCapture(1)
    if not capture.isOpened():
        raise Exception("camera not opened")

    time.sleep(2.0)
    while True:
        count = 5
        print("dsaADS")
        while count > 0:
            capture.grab()
            count -= 1
        ret, image = capture.read()
        if ret:
            try:
                position = puck_detector.detect(image, Color.YELLOW)
                cv2.circle(
                    image,
                    (
                        int(position.get_x_coordinate()),
                        int(position.get_y_coordinate()),
                    ),
                    70,
                    (0, 255, 0),
                    2,
                )
                print(position.get_x_coordinate(), position.get_y_coordinate())
            except PuckNotFoundException:
                pass
            sender.send_image(rpi_name, image)
