import time

from domain.game.GameState import GameState
from domain.game.IGameCycle import IGameCycle
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from service.communication.CommunicationService import CommunicationService
from service.game.StageService import StageService


class MasterGameCycle(IGameCycle):
    def __init__(
        self, stage_service: StageService, communication_service: CommunicationService
    ):
        self.stage_service = stage_service
        self._communication_service = communication_service

    def run(self):
        self._wait_for_robot_boot()
        self._wait_for_input()

        print("Start cycle")
        self.stage_service.execute(Stage.START_CYCLE)
        print("Go to ohmmeter \n")
        self.stage_service.execute(Stage.GO_TO_OHMMETER)
        print("Read command panel\n")
        self.stage_service.execute(Stage.READ_COMMAND_PANEL)
        print("Transport puck \n")
        self.stage_service.execute(Stage.TRANSPORT_PUCK)
        print("Stop \n")
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

    def _wait_for_robot_boot(self):
        message = self._communication_service.receive_object()
        if message.get_topic() == Topic.BOOT:
            GameState.get_instance().set_robot_booted(True)
