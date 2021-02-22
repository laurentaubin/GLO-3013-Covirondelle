from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from service.communication.CommunicationService import CommunicationService
from service.game.StageRequestRouter import StageRequestRouter


class FindCommandPanelHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        stage_request_router: StageRequestRouter,
    ):
        self.communication_service = communication_service
        self.stage_request_router = stage_request_router

    def execute(self):
        print("In FindCommandPanelHandler, sending find_command_panel start signal ...")
        self.communication_service.send_game_cycle_response(
            Stage.FIND_COMMAND_PANEL.value
        )
        self.stage_request_router.route_robot_request()
