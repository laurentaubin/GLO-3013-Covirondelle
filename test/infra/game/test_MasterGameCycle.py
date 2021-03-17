from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.game.Stage import Stage
from infra.game.MasterGameCycle import MasterGameCycle


@patch("builtins.input", lambda *args: "y")
class TestMasterGameCycle(TestCase):
    START_GAME_CYCLE = Stage.START_CYCLE
    GO_TO_OHMMETER = Stage.GO_TO_OHMMETER
    FIND_COMMAND_PANEL = Stage.FIND_COMMAND_PANEL
    TRANSPORT_PUCKS = Stage.TRANSPORT_PUCK
    GO_PARK = Stage.GO_PARK
    STOP_GAME_CYCLE = Stage.STOP

    def setUp(self) -> None:
        self.stage_service = MagicMock()

        self.master_game_cycle = MasterGameCycle(self.stage_service)

    def test_whenRun_thenStageServiceIsCalledForEachGameCycleStage(self):
        self.master_game_cycle.run()

        self.stage_service.execute.assert_any_call(self.START_GAME_CYCLE)
        self.stage_service.execute.assert_any_call(self.GO_TO_OHMMETER)
        self.stage_service.execute.assert_any_call(self.FIND_COMMAND_PANEL)
        self.stage_service.execute.assert_any_call(self.TRANSPORT_PUCKS)
        self.stage_service.execute.assert_any_call(self.GO_PARK)
        self.stage_service.execute.assert_any_call(self.STOP_GAME_CYCLE)
