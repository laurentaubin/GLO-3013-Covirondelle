from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from infra.game.MasterGameCycle import MasterGameCycle


class TestMasterGameCycle(TestCase):
    START_GAME_CYCLE = Stage.START_CYCLE
    GO_TO_OHMMETER = Stage.GO_TO_OHMMETER
    FIND_COMMAND_PANEL = Stage.READ_COMMAND_PANEL
    TRANSPORT_PUCKS = Stage.TRANSPORT_PUCK
    STOP_GAME_CYCLE = Stage.STOP

    def setUp(self) -> None:
        self.stage_service = MagicMock()
        self.communication_service = MagicMock()

        self.master_game_cycle = MasterGameCycle(
            self.stage_service, self.communication_service
        )

    @patch("domain.game.GameState.GameState.is_game_cycle_started", return_value=True)
    def test_whenRun_thenStageServiceIsCalledForEachGameCycleStage(
        self, gamestate_mock
    ):
        self.master_game_cycle.run()

        self.stage_service.execute.assert_any_call(self.START_GAME_CYCLE)
        self.stage_service.execute.assert_any_call(self.GO_TO_OHMMETER)
        self.stage_service.execute.assert_any_call(self.FIND_COMMAND_PANEL)
        self.stage_service.execute.assert_any_call(self.TRANSPORT_PUCKS)
        self.stage_service.execute.assert_any_call(self.STOP_GAME_CYCLE)

    @patch("domain.game.GameState.GameState.is_game_cycle_started", return_value=True)
    def test_whenRun_thenWaitForRobotToBoot(self, gamestate_mock):
        self.master_game_cycle.run()

        self.communication_service.receive_object.assert_called()

    @patch(
        "domain.game.GameState.GameState.is_game_cycle_started",
        MagicMock(return_value=True),
    )
    @patch("domain.game.GameState.GameState.set_robot_booted", return_value=True)
    def test_givenRobotBooted_whenRun_thenSetGameState(self, gamestate_mock):
        self.communication_service.receive_object.return_value = Message(
            Topic.BOOT, None
        )

        self.master_game_cycle.run()

        gamestate_mock.assert_called_with(True)
