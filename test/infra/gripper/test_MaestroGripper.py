from unittest import TestCase
from unittest.mock import MagicMock

from infra.gripper.MaestroGripper import MaestroGripper


class TestMaestroGripper(TestCase):
    HORIZONTAL_SERVO_ID = 0
    VERTICAL_SERVO_ID = 1
    CLOSE_GRIPPER_TARGET = 9000
    OPEN_GRIPPER_TARGET = 23213
    MOVE_GRIPPER_UP_TARGET = 21321
    MOVE_GRIPPER_DOWN_TARGET = 2312

    def setUp(self) -> None:
        self.servo_controller = MagicMock()
        self.maestro_gripper = MaestroGripper(
            self.servo_controller,
            self.HORIZONTAL_SERVO_ID,
            self.VERTICAL_SERVO_ID,
            self.CLOSE_GRIPPER_TARGET,
            self.OPEN_GRIPPER_TARGET,
            self.MOVE_GRIPPER_UP_TARGET,
            self.MOVE_GRIPPER_DOWN_TARGET,
        )

    def test_whenClose_thenServoControllerIsUsedToCloseGripper(self):
        self.maestro_gripper.close()

        self.servo_controller.setTarget.assert_called_with(
            self.HORIZONTAL_SERVO_ID, self.CLOSE_GRIPPER_TARGET
        )

    def test_whenOpen_thenServoControllerIsUsedToOpenGripper(self):
        self.maestro_gripper.open()

        self.servo_controller.setTarget.assert_called_with(
            self.HORIZONTAL_SERVO_ID, self.OPEN_GRIPPER_TARGET
        )

    def test_whenMoveUp_thenServoControllerIsUsedToMoveGripperUp(self):
        self.maestro_gripper.elevate()

        self.servo_controller.setTarget.assert_called_with(
            self.VERTICAL_SERVO_ID, self.MOVE_GRIPPER_UP_TARGET
        )

    def test_whenMoveDown_thenServoControllerIsUsedToMoveGripperDown(self):
        self.maestro_gripper.lower()

        self.servo_controller.setTarget.assert_called_with(
            self.VERTICAL_SERVO_ID, self.MOVE_GRIPPER_DOWN_TARGET
        )
