import time

from domain.game.IGameCycle import IGameCycle
from domain.game.Stage import Stage
from service.communication.CommunicationService import CommunicationService
from service.game.StageRequestRouter import StageRequestRouter
from service.game.StageService import StageService


class MasterGameCycle(IGameCycle):
    def __init__(
        self,
        communication_service: CommunicationService,
        stage_request_router: StageRequestRouter,
        stage_service: StageService,
    ):
        self.communication_service = communication_service
        self.stage_request_router = stage_request_router
        self.stage_service = stage_service

    def run(self):
        self._send_start_signal()
        print("\n")
        self.stage_service.execute(Stage.GO_TO_OHMMETER)
        print("\n")
        self.stage_service.execute(Stage.FIND_COMMAND_PANEL)
        print("\n")
        self.stage_service.execute(Stage.TRANSPORT_PUCK)
        print("\n")
        self.stage_service.execute(Stage.GO_PARK)
        print("\n")
        self.stage_service.execute(Stage.STOP)
        print("\n")

        print("Game cycle complete!")

    def stop(self):
        pass

    def _send_start_signal(self):
        while True:
            start_signal = input("send start signal (y/n): ")
            if start_signal == "y":
                break
        self.communication_service.send_game_cycle_response(Stage.START_CYCLE.value)
        time.sleep(1)
        self.communication_service.receive_game_cycle_request()
