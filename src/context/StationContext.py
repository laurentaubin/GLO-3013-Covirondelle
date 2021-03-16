from cv2.aruco import DICT_4X4_50

from application.ApplicationServer import ApplicationServer
from application.RobotStatusReceiver import RobotStatusReceiver
from config.config import (
    SOCKET_DOCKER_ADDRESS,
    PING_PORT,
    SOCKET_ANY_ADDRESS,
    GAME_CYCLE_PORT,
    CALIBRATION_FILE_PATH,
    ROBOT_ARUCO_MARKER_ID,
    LAPTOP_CAMERA_INDEX,
    BASE_TABLE_IMAGE,
)
from domain.pathfinding.AStarShortestPathAlgorithm import AStarShortestPathAlgorithm
from infra.camera.ImageBasedWorldCamera import ImageBasedWorldCamera
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera
from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from infra.communication.socket.ReqRepSocketConnector import ReqRepSocketConnector
from infra.game.MasterGameCycle import MasterGameCycle
from infra.vision.OpenCvRobotDetector import OpenCvRobotDetector
from infra.vision.OpenCvStartingZoneDetector import OpenCvStartingZoneDetector
from infra.vision.OpenCvTableDetector import OpenCvTableDetector
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
        self._local_flag = local_flag
        self._game_cycle_connector, self._pub_sub_connector = self._create_connectors()
        self._communication_service = CommunicationService(
            self._game_cycle_connector, self._pub_sub_connector
        )

        self._vision_service = self._create_vision_service()

        self._shortest_path_algorithm = AStarShortestPathAlgorithm()
        self._path_service = PathService(
            self._vision_service,
            self._communication_service,
            self._shortest_path_algorithm,
        )
        self._stage_request_router = StageRequestRouter(
            self._communication_service, self._path_service
        )

        self._stage_service = self._create_stage_service()

        self._game_cycle = MasterGameCycle(
            self._communication_service, self._stage_request_router, self._stage_service
        )

        self._robot_status_receiver = RobotStatusReceiver(self._communication_service)
        self._application_server = ApplicationServer(
            self._robot_status_receiver, self._game_cycle
        )

    def run(self):
        self._application_server.run()

    def _create_connectors(self):
        if self._local_flag:
            game_cycle_connector = ReqRepSocketConnector(
                SOCKET_DOCKER_ADDRESS + GAME_CYCLE_PORT
            )
            pub_sub_connector = PubSubConnector(SOCKET_DOCKER_ADDRESS + PING_PORT)
            return game_cycle_connector, pub_sub_connector

        game_cycle_connector = ReqRepSocketConnector(
            SOCKET_ANY_ADDRESS + GAME_CYCLE_PORT
        )
        pub_sub_connector = PubSubConnector(SOCKET_ANY_ADDRESS + PING_PORT)
        return game_cycle_connector, pub_sub_connector

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
            self._communication_service, self._stage_request_router
        )

    def _create_find_command_panel_handler(self):
        return FindCommandPanelHandler(
            self._communication_service, self._stage_request_router
        )

    def _create_transport_puck_handler(self):
        return TransportPuckHandler(
            self._communication_service, self._stage_request_router
        )

    def _create_go_park_handler(self):
        return GoParkHandler(self._communication_service, self._stage_request_router)

    def _create_stop_handler(self):
        return StopHandler(self._communication_service, self._stage_request_router)

    def _create_vision_service(self):
        starting_zone_corners_detector = OpenCvStartingZoneDetector()
        table_detector = OpenCvTableDetector()
        world_camera = self._create_world_camera()
        robot_detector = OpenCvRobotDetector(DICT_4X4_50, ROBOT_ARUCO_MARKER_ID)
        return VisionService(
            starting_zone_corners_detector, table_detector, world_camera, robot_detector
        )

    def _create_world_camera(self):
        camera_calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
        if self._local_flag:
            return ImageBasedWorldCamera(BASE_TABLE_IMAGE)

        return OpenCvWorldCamera(LAPTOP_CAMERA_INDEX, camera_calibrator)
