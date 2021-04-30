from unittest.mock import MagicMock

from config.config import (
    MAESTRO_POLULU_PORT_NAME,
    SERVO_SPEED,
    SERVO_ACCELERATION,
    GRIPPER_HORIZONTAL_SERVO_ID,
    GRIPPER_VERTICAL_SERVO_ID,
    CAMERA_HORIZONTAL_SERVO_ID,
    CAMERA_VERTICAL_SERVO_ID,
    HORIZONTAL_ANGLE_RANGE,
    VERTICAL_ANGLE_RANGE,
    CAMERA_INDEX,
    CAMERA_LOOK_UP_TARGET,
    CAMERA_LOOK_DOWN_TARGET,
)
from infra.MaestroController import MaestroController
from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera
from service.vision.VisionService import VisionService


def configure_maestro_channel(maestro, channel_id):
    maestro.setSpeed(channel_id, SERVO_SPEED)
    maestro.setAccel(channel_id, SERVO_ACCELERATION)


if __name__ == "__main__":
    maestro = MaestroController(ttyStr=MAESTRO_POLULU_PORT_NAME)

    configure_maestro_channel(maestro, GRIPPER_HORIZONTAL_SERVO_ID)
    configure_maestro_channel(maestro, GRIPPER_VERTICAL_SERVO_ID)
    configure_maestro_channel(maestro, CAMERA_HORIZONTAL_SERVO_ID)
    configure_maestro_channel(maestro, CAMERA_VERTICAL_SERVO_ID)
    embedded_camera = OpenCvEmbeddedCamera(
        CAMERA_INDEX,
        maestro,
        CAMERA_HORIZONTAL_SERVO_ID,
        CAMERA_VERTICAL_SERVO_ID,
        HORIZONTAL_ANGLE_RANGE,
        VERTICAL_ANGLE_RANGE,
    )
    letter_position_detector = MagicMock()

    vision_service = VisionService(
        embedded_camera,
        letter_position_detector,
        CAMERA_LOOK_DOWN_TARGET,
        CAMERA_LOOK_UP_TARGET,
    )

    print("-------------- Press to look left ----------------")
    input("Press Enter to start test")
    vision_service.rotate_camera_horizontally(5000)

    print("-------------- Press to look middle ----------------")
    input("Press Enter to start test")
    vision_service.rotate_camera_horizontally(6200)

    print("-------------- Press to make camera look up ----------------")
    input("Press Enter to start test")
    vision_service.make_camera_look_up()

    print("-------------- Press to make camera look down ----------------")
    input("Press Enter to start test")
    vision_service.make_camera_look_down()
