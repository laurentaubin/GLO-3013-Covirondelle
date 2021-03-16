from unittest import TestCase
from unittest.mock import MagicMock, patch

from application.VisionWorker import VisionWorker


class TestVisionWorker(TestCase):
    A_TABLE_IMAGE = MagicMock()
    A_ROBOT_POSE = MagicMock()

    def setUp(self):
        self.vision_service = MagicMock()
        self.vision_worker = VisionWorker(self.vision_service)

    @patch("domain.game.GameState.GameState.set_robot_pose")
    def test_whenUpdateVisionState_thenGameStateRobotPoseIsUpdated(
        self, gameStateSetRobotPose_mock
    ):
        self.vision_service.get_vision_state.return_value = (
            self.A_TABLE_IMAGE,
            self.A_ROBOT_POSE,
        )

        self.vision_worker.update_vision_state(self.vision_service)

        gameStateSetRobotPose_mock.assert_called_with(self.A_ROBOT_POSE)

    @patch("domain.game.GameState.GameState.set_table_image")
    def test_whenUpdateVisionState_thenGameStateTableImageIsUpdated(
        self, gameStateSetTableImage_mock
    ):
        self.vision_service.get_vision_state.return_value = (
            self.A_TABLE_IMAGE,
            self.A_ROBOT_POSE,
        )

        self.vision_worker.update_vision_state(self.vision_service)

        gameStateSetTableImage_mock.assert_called_with(self.A_TABLE_IMAGE)
