from config.config import (
    MAESTRO_POLULU_PORT_NAME,
    SERVO_SPEED,
    SERVO_ACCELERATION,
    GRIPPER_HORIZONTAL_SERVO_ID,
    GRIPPER_VERTICAL_SERVO_ID,
    CAMERA_HORIZONTAL_SERVO_ID,
    CAMERA_VERTICAL_SERVO_ID,
    OPEN_GRIPPER_TARGET,
    CLOSE_GRIPPER_TARGET,
    MOVE_GRIPPER_UP_TARGET,
    MOVE_GRIPPER_DOWN_TARGET,
)
from infra.MaestroController import MaestroController
from infra.gripper.MaestroGripper import MaestroGripper
from service.gripper.GripperService import GripperService


def configure_maestro_channel(_maestro, channel_id):
    _maestro.setSpeed(channel_id, SERVO_SPEED)
    _maestro.setAccel(channel_id, SERVO_ACCELERATION)


if __name__ == "__main__":
    maestro = MaestroController(ttyStr=MAESTRO_POLULU_PORT_NAME)

    configure_maestro_channel(maestro, GRIPPER_HORIZONTAL_SERVO_ID)
    configure_maestro_channel(maestro, GRIPPER_VERTICAL_SERVO_ID)
    configure_maestro_channel(maestro, CAMERA_HORIZONTAL_SERVO_ID)
    configure_maestro_channel(maestro, CAMERA_VERTICAL_SERVO_ID)

    gripper = MaestroGripper(
        maestro,
        GRIPPER_HORIZONTAL_SERVO_ID,
        GRIPPER_VERTICAL_SERVO_ID,
        OPEN_GRIPPER_TARGET,
        CLOSE_GRIPPER_TARGET,
        MOVE_GRIPPER_UP_TARGET,
        MOVE_GRIPPER_DOWN_TARGET,
    )

    gripper_service = GripperService(gripper)

    print("-------------- Close gripper test ----------------")
    input("Press Enter to start test")
    gripper_service.close_gripper()

    print("-------------- Open gripper test ----------------")
    input("Press Enter to start test")
    gripper_service.open_gripper()

    print("-------------- Move gripper up test ----------------")
    input("Press Enter to start test")
    gripper_service.elevate_gripper()

    print("-------------- Move gripper down test ----------------")
    input("Press Enter to start test")
    gripper_service.lower_gripper()
