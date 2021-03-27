# Station communication
SOCKET_DOCKER_BASE_ADDRESS = "tcp://covirondelle-station:"
SOCKET_LOCAL_BASE_ADDRESS = "tcp://localhost:"
PING_PORT = "5555"
# TODO Replace with IP address of station when at the lab
SOCKET_STATION_ADDRESS = "tcp://192.168.0.119:"
GAME_CYCLE_PORT = "5556"

# Vision
TESSERACT_LOCATION = "/usr/bin/tesseract"
PIXEL_TO_CENTIMETERS = 6
# TODO Change for real values after testing in lab and with real images
PUCK_ALIGNMENT_X_CENTER_POSITION = 320
PUCK_ALIGNMENT_Y_CENTER_POSITION = 340
PUCK_ALIGNMENT_THRESHOLD = 50
STARTING_ZONE_X_CENTER_POSITION = 349
OHMMETER_ALIGNMENT_THRESHOLD = 10

# STM-32
# TODO change port_name when on rpi
STM_PORT_NAME = "/dev/ttySTM32"
STM_BAUD_RATE = 115200

# Robot movement
# TODO test at lab to find optimal values
ROBOT_RADIUS = 0.1075
ROBOT_ROTATION_SPEED = 0.15
ROBOT_MAXIMUM_SPEED = 0.25
ROBOT_ALIGNMENT_SPEED = 0.02
SERVOING_CONSTANT = 5
BASE_COMMAND_DURATION = 0.1

# Maestro polulu
# TODO Change maestro port name
MAESTRO_POLULU_PORT_NAME = "/dev/ttyMAESTRO"
GRIPPER_HORIZONTAL_SERVO_ID = 0
GRIPPER_VERTICAL_SERVO_ID = 1
CAMERA_HORIZONTAL_SERVO_ID = 2
CAMERA_VERTICAL_SERVO_ID = 3
SERVO_SPEED = 60
SERVO_ACCELERATION = 10

# Camera
CAMERA_INDEX = 0
EMBEDDED_CAMERA_IMAGE_SIZE = (640, 480)

# Camera servos
MAX_HORIZONTAL_ANGLE_VALUE = 9000
MIN_HORIZONTAL_ANGLE_VALUE: int = 5000
HORIZONTAL_ANGLE_RANGE = (MIN_HORIZONTAL_ANGLE_VALUE, MAX_HORIZONTAL_ANGLE_VALUE)
MIN_VERTICAL_ANGLE_VALUE = 9000
MAX_VERTICAL_ANGLE_VALUE = 5000
VERTICAL_ANGLE_RANGE = (MIN_VERTICAL_ANGLE_VALUE, MAX_VERTICAL_ANGLE_VALUE)

# Gripper servos
OPEN_GRIPPER_TARGET = 9000
CLOSE_GRIPPER_TARGET = 5000
MOVE_GRIPPER_UP_TARGET = 5000
MOVE_GRIPPER_DOWN_TARGET = 9000

# Gripper
CURRENT_CONSUMPTION_THRESHOLD = 300
