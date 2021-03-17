from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.game.Stage import Stage
from service.handler.StartCycleHandler import StartCycleHandler


@patch("time.sleep", MagicMock())
class TestStartCycleHandler(TestCase):
    A_GAME_TABLE = MagicMock()

    def setUp(self) -> None:
        self.communication_service = MagicMock()
        self.path_service = MagicMock()
        self.vision_service = MagicMock()

        self.start_cycle_handler = StartCycleHandler(
            self.communication_service,
            self.path_service,
            self.vision_service,
        )

    @patch("domain.game.GameState.GameState.set_current_stage")
    def test_whenExecute_thenGameStateIsUpdatedWithStartGameStage(self, gameState_mock):
        start_cycle_stage = Stage.START_CYCLE

        self.start_cycle_handler.execute()

        gameState_mock.assert_called_with(start_cycle_stage)

    def test_givenGameTableCreatedByVisionService_whenExecute_thenGameTableIsSetInPathService(
        self,
    ):
        self.vision_service.create_game_table.return_value = self.A_GAME_TABLE

        self.start_cycle_handler.execute()

        self.path_service.set_game_table.assert_called_with(self.A_GAME_TABLE)

    @patch("domain.game.GameState.GameState.set_game_table")
    def test_givenGameTableCreatedByVisionService_whenExecute_thenGameStateIsUpdatedWithGameTable(
        self, gameState_mock
    ):
        self.vision_service.create_game_table.return_value = self.A_GAME_TABLE

        self.start_cycle_handler.execute()

        gameState_mock.assert_called_with(self.A_GAME_TABLE)

    def test_whenExecute_thenStartSignalIsSentToRobot(self):
        start_signal = Stage.START_CYCLE.value

        self.start_cycle_handler.execute()

        self.communication_service.send_game_cycle_response.assert_called_with(
            start_signal
        )

    def test_whenExecute_thenRobotResponseIsHandled(self):
        self.start_cycle_handler.execute()

        self.communication_service.receive_game_cycle_request.assert_called()
