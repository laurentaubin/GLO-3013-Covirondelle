import time

from domain.communication.Message import Message
from domain.game.GameState import GameState
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
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
        self._communication_service.send_object(
            Message(Topic.START_CYCLE, Stage.START_CYCLE)
        )
        time.sleep(1)

    def _route_robot_response(self):
        message = self._communication_service.receive_object()

        if message.get_payload() == Stage.STAGE_COMPLETED:
            return

        print("Whoops, robot sent the wrong thing")
