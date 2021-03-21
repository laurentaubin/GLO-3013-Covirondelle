import time

from domain.game.GameState import GameState
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from service.communication.CommunicationService import CommunicationService
from service.path.PathService import PathService
from service.vision.VisionService import VisionService


class StartCycleHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        path_service: PathService,
        vision_service: VisionService,
    ):
        self._communication_service = communication_service
        self._path_service = path_service
        self._vision_service = vision_service

    def execute(self):
        GameState.get_instance().set_current_stage(Stage.START_CYCLE)

        self._create_game_table()
        self._send_start_signal()
        self._route_robot_response()

    def _create_game_table(self):
        game_table = self._vision_service.create_game_table()
        self._path_service.set_game_table(game_table)
        GameState.get_instance().set_game_table(game_table)

    def _send_start_signal(self):
        print("Sending start signal...")
        self._communication_service.send_game_cycle_response(Stage.START_CYCLE.value)
        time.sleep(1)

    def _route_robot_response(self):
        response = self._communication_service.receive_game_cycle_request()

        if response == Stage.STAGE_COMPLETED.value:
            return

        print("Whoops, robot sent the wrong thing")
