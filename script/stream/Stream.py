# https://pypi.org/project/imagezmq/

import cv2
import imagezmq

from config.config import SOCKET_ANY_ADDRESS, STREAM_PI_FEED_PORT

image_hub = imagezmq.ImageHub(open_port=SOCKET_ANY_ADDRESS + STREAM_PI_FEED_PORT)

if __name__ == "__main__":
    while True:
        rpi_name, image = image_hub.recv_image()
        cv2.imshow(rpi_name, image)
        cv2.waitKey(1)
        image_hub.send_reply(b"OK")
