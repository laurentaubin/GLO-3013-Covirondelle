# https://pypi.org/project/imagezmq/

import socket
import time

import imagezmq
from imutils.video import VideoStream

from config.config import SOCKET_STATION_ADDRESS, STREAM_PI_FEED_PORT

sender = imagezmq.ImageSender(connect_to=SOCKET_STATION_ADDRESS + STREAM_PI_FEED_PORT)

rpi_name = socket.gethostname()
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
while True:
    image = picam.read()
    sender.send_image(rpi_name, image)
