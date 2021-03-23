from domain.IGripper import IGripper
from infra.IServoController import IServoController


class MaestroGripper(IGripper):
    def __init__(
        self,
        servo_controller: IServoController,
        horizontal_servo_id: int,
        vertical_servo_id: int,
        close_gripper_target: int,
        open_griper_target: int,
        move_gripper_up: int,
        move_gripper_down: int,
    ):
        self._servo_controller = servo_controller
        self._horizontal_servo_id = horizontal_servo_id
        self._vertical_servo_id = vertical_servo_id
        self._close_gripper_target = close_gripper_target
        self._open_gripper_target = open_griper_target
        self._move_gripper_up = move_gripper_up
        self._move_gripper_down = move_gripper_down

    def close(self) -> None:
        self._servo_controller.setTarget(
            self._horizontal_servo_id, self._close_gripper_target
        )

    def open(self) -> None:
        self._servo_controller.setTarget(
            self._horizontal_servo_id, self._open_gripper_target
        )

    def elevate(self) -> None:
        self._servo_controller.setTarget(self._vertical_servo_id, self._move_gripper_up)

    def lower(self) -> None:
        self._servo_controller.setTarget(
            self._vertical_servo_id, self._move_gripper_down
        )
