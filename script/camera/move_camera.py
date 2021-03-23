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
)
from infra.MaestroController import MaestroController
from infra.camera.MaestroEmbeddedCamera import MaestroEmbeddedCamera
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
    embedded_camera = MaestroEmbeddedCamera(
        maestro,
        CAMERA_HORIZONTAL_SERVO_ID,
        CAMERA_VERTICAL_SERVO_ID,
        HORIZONTAL_ANGLE_RANGE,
        VERTICAL_ANGLE_RANGE,
    )
    letter_position_detector = MagicMock()

    vision_service = VisionService(embedded_camera, letter_position_detector)

    print("-------------- Horizontal Movement test ----------------")
    input("Press Enter to start test")
    vision_service.rotate_camera_horizontally(20)

    print("-------------- Vertical Movement test ----------------")
    input("Press Enter to start test")
    vision_service.rotate_camera_vertically(20)
