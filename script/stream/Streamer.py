# https://pypi.org/project/imagezmq/

import socket
import time

import cv2
import imagezmq

from domain.Color import Color
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector

if __name__ == "__main__":
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 500)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    sender = imagezmq.ImageSender(connect_to="tcp://10.240.80.139:5557")
    puck_detector = OpenCvPuckDetector()

    rpi_name = socket.gethostname()
    capture = None
    for i in range(20):
        capture = cv2.VideoCapture(0)
        if capture.isOpened():
            break

    time.sleep(2.0)
    while True:
        count = 4
        print("dsaADS")
        while count > 0:
            capture.grab()
            count -= 1
        ret, image = capture.read()
        if ret:
            try:
                position = puck_detector.detect(image, Color.WHITE)
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
                print("puck not found")
                pass
        print("sending")
        sender.send_image(rpi_name, image)
