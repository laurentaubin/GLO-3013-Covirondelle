import os

import numpy as np

SOCKET_DOCKER_ADDRESS = "tcp://0.0.0.0:"
PING_PORT = "5555"

SOCKET_ANY_ADDRESS = "tcp://*:"
GAME_CYCLE_PORT = "5556"
STREAM_PI_FEED_PORT = "5557"

# TODO Test at lab to find right radii value
ROBOT_RADIUS = 100
OBSTACLE_RADIUS = 30

CALIBRATION_FILE_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/numpy-1600x1200.npz"
)

LAPTOP_CAMERA_INDEX = 1
PC_CAMERA_INDEX = 1

PIXEL_TO_METERS_RATIO = 643
PIXEL_TO_CENTIMETERS_RATIO = 6.43

OBSTACLE_ARUCO_MARKER_ID = 0
# in meter
OBSTACLE_ARUCO_MARKER_SIZE = 0.08
NUMBER_OF_OBSTACLES = 2
ROBOT_ARUCO_MARKER_ID = 1
CALIBRATION_ARRAYS = np.load(CALIBRATION_FILE_PATH)
CAMERA_MATRIX = CALIBRATION_ARRAYS["camera_matrix"]
DISTORTION_COEFFICIENTS = CALIBRATION_ARRAYS["distortion_coefficients"]

WORLD_CAMERA_IMAGE_SIZE = (1600, 1200)

# in meter
OBSTACLE_HEIGHT = 0.304

BASE_TABLE_IMAGE = (
    os.path.dirname(os.path.abspath(__file__))
    + "/../../resources/test/puck-detector-test-marker-3.jpg"
)

DEFAULT_OHMMETER_POSITION = 20, 20
