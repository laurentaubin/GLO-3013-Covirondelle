from application.ApplicationServer import ApplicationServer
from application.RobotStatusReceiver import RobotStatusReceiver
from config.config import (
    SOCKET_DOCKER_ADDRESS,
    PING_PORT,
    SOCKET_ANY_ADDRESS,
    GAME_CYCLE_PORT,
    CALIBRATION_FILE_PATH,
)
from domain.pathfinding.AStarShortestPathAlgorithm import AStarShortestPathAlgorithm
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from infra.communication.socket.ReqRepSocketConnector import ReqRepSocketConnector
from infra.game.MasterGameCycle import MasterGameCycle
from infra.vision.OpenCvStartingZoneDetector import OpenCvStartingZoneDetector
from service.communication.CommunicationService import CommunicationService
from service.game.StageHandlerSelector import StageHandlerSelector
from service.game.StageRequestRouter import StageRequestRouter
from service.game.StageService import StageService
from service.handler.FindCommandPanelHandler import FindCommandPanelHandler
from service.handler.GoParkHandler import GoParkHandler
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler
from service.handler.StopHandler import StopHandler
from service.handler.TransportPuckHandler import TransportPuckHandler
from service.path.PathService import PathService
from service.vision.VisionService import VisionService


class StationContext:
    def __init__(self, local_flag):
        if local_flag:
            self.game_cycle_connector = ReqRepSocketConnector(
                SOCKET_DOCKER_ADDRESS + GAME_CYCLE_PORT
            )
            self.pub_sub_connector = PubSubConnector(SOCKET_DOCKER_ADDRESS + PING_PORT)
        else:
            self.game_cycle_connector = ReqRepSocketConnector(
                SOCKET_ANY_ADDRESS + GAME_CYCLE_PORT
            )
            self.pub_sub_connector = PubSubConnector(SOCKET_ANY_ADDRESS + PING_PORT)

        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.pub_sub_connector
        )
        self.vision_service = self._create_vision_service()

        # TODO Instantiate algorithm with non empty maze
        self.shortest_path_algorithm = AStarShortestPathAlgorithm(None)
        self.path_service = PathService(
            self.vision_service,
            self.communication_service,
            self.shortest_path_algorithm,
        )
        self.stage_request_router = StageRequestRouter(
            self.communication_service, self.path_service
        )

        self.stage_service = self._create_stage_service()

        self.game_cycle = MasterGameCycle(
            self.communication_service, self.stage_request_router, self.stage_service
        )

        self.robot_status_receiver = RobotStatusReceiver(self.communication_service)
        self.application_server = ApplicationServer(
            self.robot_status_receiver, self.game_cycle
        )

    def run(self):
        self.application_server.run()

    def _create_stage_service(self):
        self.stage_handler_selector = self._create_stage_handler_selector()
        return StageService(self.stage_handler_selector)

    def _create_stage_handler_selector(self):
        go_to_ohmmeter_handler = self._create_go_to_ohmmeter_handler()
        find_command_panel_handler = self._create_find_command_panel_handler()
        transport_puck_handler = self._create_transport_puck_handler()
        go_park_handler = self._create_go_park_handler()
        stop_handler = self._create_stop_handler()
        return StageHandlerSelector(
            go_to_ohmmeter_handler,
            find_command_panel_handler,
            transport_puck_handler,
            go_park_handler,
            stop_handler,
        )

    def _create_go_to_ohmmeter_handler(self):
        return GoToOhmmeterHandler(
            self.communication_service, self.stage_request_router
        )

    def _create_find_command_panel_handler(self):
        return FindCommandPanelHandler(
            self.communication_service, self.stage_request_router
        )

    def _create_transport_puck_handler(self):
        return TransportPuckHandler(
            self.communication_service, self.stage_request_router
        )

    def _create_go_park_handler(self):
        return GoParkHandler(self.communication_service, self.stage_request_router)

    def _create_stop_handler(self):
        return StopHandler(self.communication_service, self.stage_request_router)

    def _create_vision_service(self):
        starting_zone_corners_detector = OpenCvStartingZoneDetector()
        image_calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
        return VisionService(starting_zone_corners_detector, image_calibrator)
