from domain.game.GameState import GameState
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from service.communication.CommunicationService import CommunicationService
from service.path.PathService import PathService
from service.vision.VisionService import VisionService


class GoToOhmmeterHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        vision_service: VisionService,
        path_service: PathService,
    ):
        self._communication_service = communication_service
        self._vision_service = vision_service
        self._path_service = path_service

    def execute(self):
        print("In GoToOhmmeter, sending go_to_ohmmeter start signal ...")
        GameState.get_instance().set_current_stage(Stage.GO_TO_OHMMETER)

        self._communication_service.send_game_cycle_response(Stage.GO_TO_OHMMETER.value)
        self._route_robot_response()

        robot_pose = GameState.get_instance().get_robot_pose()
        path = self._path_service.find_path_to_ohmmeter(robot_pose.get_position())

        self._communication_service.send_object(path)
        resistance_value = self._communication_service.receive_object()

        GameState.get_instance().set_resistance_value(resistance_value)

        self._communication_service.send_game_cycle_response(
            Stage.STAGE_COMPLETED.value
        )
        self._route_robot_response()

    def _route_robot_response(self):
        game_cycle = self._communication_service.receive_game_cycle_request()

        if game_cycle == Stage.GO_TO_OHMMETER.value:
            pass
        elif game_cycle == Stage.STAGE_COMPLETED.value:
            pass
        else:
            print("whoops")
