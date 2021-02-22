from domain.game.Stage import Stage
from service.communication.CommunicationService import CommunicationService
from service.path.PathService import PathService


class StageRequestRouter:
    def __init__(
        self, communication_service: CommunicationService, path_service: PathService
    ):
        self.communication_service = communication_service
        self.path_service = path_service

    def route_robot_request(self):
        while True:
            request = self.communication_service.receive_game_cycle_request()
            if request == Stage.STAGE_COMPLETED.value:
                break
            request_response = self._route(request)
            self.communication_service.send_game_cycle_response(request_response)

    def _route(self, request):
        # Route request to the right service, example:
        # if (request == GameCycleRequest.GET_PATH_TO_OHMMETER):
        #       return self.path_service.get_path_to_ohmmeter
        return "response"
