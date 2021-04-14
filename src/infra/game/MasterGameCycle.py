import time

from domain.game.GameState import GameState
from domain.game.IGameCycle import IGameCycle
from domain.game.Stage import Stage
from service.game.StageService import StageService


class MasterGameCycle(IGameCycle):
    def __init__(
        self,
        stage_service: StageService,
    ):
        self.stage_service = stage_service

    def run(self):
        self._wait_for_input()

        self.stage_service.execute(Stage.START_CYCLE)
        print("\n")
        self.stage_service.execute(Stage.GO_TO_OHMMETER)
        print("\n")
        self.stage_service.execute(Stage.FIND_COMMAND_PANEL)
        print("\n")
        self.stage_service.execute(Stage.TRANSPORT_PUCK)
        print("\n")
        self.stage_service.execute(Stage.STOP)
        print("\n")

        print("Game cycle complete!")

    def stop(self):
        pass

    def _wait_for_input(self):
        game_state: GameState = GameState.get_instance()
        while True:
            if game_state.is_game_cycle_started():
                break
            time.sleep(0.5)
