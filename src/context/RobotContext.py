from application.ApplicationServer import ApplicationServer
from application.CommunicationRunner import CommunicationRunner
from config.config import SOCKET_DOCKER_BASE_ADDRESS, PING_PORT, SOCKET_STATION_ADDRESS, GAME_CYCLE_PORT
from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from infra.communication.socket.ReqRepSocketConnector import ReqRepSocketConnector
from infra.game.SlaveGameCycle import SlaveGameCycle
from service.communication.CommunicationService import CommunicationService
from service.game.StageHandlerSelector import StageHandlerSelector
from service.game.StageService import StageService
from service.handler.FindCommandPanelHandler import FindCommandPanelHandler
from service.handler.GoParkHandler import GoParkHandler
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler
from service.handler.StopHandler import StopHandler
from service.handler.TransportPuckHandler import TransportPuckHandler
from service.mouvement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService


class RobotContext:
    def __init__(self, local_flag):
        if local_flag:
            self.game_cycle_connector = ReqRepSocketConnector(SOCKET_DOCKER_BASE_ADDRESS + GAME_CYCLE_PORT)
            self.pub_sub_connector = PubSubConnector(SOCKET_DOCKER_BASE_ADDRESS + PING_PORT)
        else:
            self.game_cycle_connector = ReqRepSocketConnector(SOCKET_STATION_ADDRESS + GAME_CYCLE_PORT)
            self.pub_sub_connector = PubSubConnector(SOCKET_STATION_ADDRESS + PING_PORT)

        self.communication_service = CommunicationService(self.game_cycle_connector, self.pub_sub_connector)
        self.movement_service = MovementService()

        self.stage_service = self._create_stage_service()
        self.slave_game_cycle = SlaveGameCycle(self.communication_service, self.stage_service)

        self.communication_runner = CommunicationRunner(self.communication_service)

        self.application_server = ApplicationServer(self.communication_runner, self.slave_game_cycle)

    def run(self):
        self.application_server.run()

    def _create_stage_service(self):
        stage_selector = self._create_stage_handler_selector()

        return StageService(stage_selector)

    def _create_stage_handler_selector(self):
        resistance_service = ResistanceService()
        go_to_ohmmeter_handler = GoToOhmmeterHandler(
            communication_service=self.communication_service,
            movement_service=self.movement_service,
            resistance_service=resistance_service,
        )
        find_command_panel_handler = FindCommandPanelHandler()
        transport_puck_handler = TransportPuckHandler()
        go_park_handler = GoParkHandler()
        stop_handler = StopHandler()

        return StageHandlerSelector(go_to_ohmmeter_handler, find_command_panel_handler, transport_puck_handler,
                                    go_park_handler, stop_handler)
