from unittest import TestCase
from unittest.mock import MagicMock

from service.gripper.GripperService import GripperService


class TestGripperService(TestCase):
    def setUp(self) -> None:
        self.gripper = MagicMock()
        self.gripper_service = GripperService(self.gripper)

    def test_whenOpenGripper_thenGripperIsOpened(self):
        self.gripper_service.open_gripper()

        self.gripper.open.assert_called_once()

    def test_whenCloseGripper_thenGripperIsClosed(self):
        self.gripper_service.close_gripper()

        self.gripper.close.assert_called_once()

    def test_whenElevateGripper_thenGripperIsElevated(self):
        self.gripper_service.elevate_gripper()

        self.gripper.elevate.assert_called_once()

    def test_whenLowerGripper_thenGripperIsMovedLowered(self):
        self.gripper_service.lower_gripper()

        self.gripper.lower.assert_called_once()
