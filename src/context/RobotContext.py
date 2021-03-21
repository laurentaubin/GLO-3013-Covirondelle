import serial

from application.ApplicationServer import ApplicationServer
from application.CommunicationRunner import CommunicationRunner
from config.config import (
    PING_PORT,
    SOCKET_STATION_ADDRESS,
    GAME_CYCLE_PORT,
    STM_PORT_NAME,
    STM_BAUD_RATE,
    ROBOT_MAXIMUM_SPEED,
    SERVOING_CONSTANT,
    BASE_COMMAND_DURATION,
    SOCKET_LOCAL_BASE_ADDRESS,
    HORIZONTAL_SERVO_ID,
    VERTICAL_SERVO_ID,
    SERVO_SPEED,
    SERVO_ACCELERATION,
    HORIZONTAL_ANGLE_RANGE,
    VERTICAL_ANGLE_RANGE,
    MAESTRO_POLULU_PORT_NAME,
)
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.MovementFactory import MovementFactory
from infra.communication.camera.IServoController import IServoController
from infra.communication.camera.MaestroController import MaestroController
from infra.communication.camera.MaestroEmbeddedCamera import MaestroEmbeddedCamera
from infra.communication.motor_controller.FakeMotorController import FakeMotorController
from infra.communication.motor_controller.StmMotorController import StmMotorController
from infra.communication.station.ZmqPublisherConnector import ZmqPublisherConnector
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector
from infra.game.SlaveGameCycle import SlaveGameCycle
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)
from service.communication.CommunicationService import CommunicationService
from service.game.StageHandlerSelector import StageHandlerSelector
from service.game.StageService import StageService
from service.handler.FindCommandPanelHandler import FindCommandPanelHandler
from service.handler.GoParkHandler import GoParkHandler
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler
from service.handler.StopHandler import StopHandler
from service.handler.TransportPuckHandler import TransportPuckHandler
from service.movement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService
from service.vision.VisionService import VisionService


class RobotContext:
    def __init__(self, local_flag):
        self._local_flag = local_flag

        self._communication_service = self._create_communication_service()
        self._movement_service = self._create_movement_service()
        self._vision_service = self._create_vision_service()

        self.stage_service = self._create_stage_service()
        self.slave_game_cycle = SlaveGameCycle(
            self._communication_service, self.stage_service
        )

        self.communication_runner = CommunicationRunner(self._communication_service)

        self.application_server = ApplicationServer(
            self.communication_runner, self.slave_game_cycle
        )

    def _create_communication_service(self):
        game_cycle_connector, pub_sub_connector = self._create_connectors()
        return CommunicationService(game_cycle_connector, pub_sub_connector)

    def _create_movement_service(self):
        movement_command_factory = MovementCommandFactory(
            ROBOT_MAXIMUM_SPEED,
            SERVOING_CONSTANT,
            BASE_COMMAND_DURATION,
        )
        motor_controller = self._create_motor_controller(movement_command_factory)
        movement_factory = MovementFactory()
        return MovementService(movement_factory, motor_controller)

    def _create_motor_controller(self, movement_command_factory):
        if self._local_flag:
            return FakeMotorController()

        return StmMotorController(
            serial.Serial(port=STM_PORT_NAME, baudrate=STM_BAUD_RATE),
            movement_command_factory,
        )

    def _create_connectors(self):
        if self._local_flag:
            game_cycle_connector = ZmqReqRepConnector(
                SOCKET_LOCAL_BASE_ADDRESS + GAME_CYCLE_PORT
            )
            publisher_connector = ZmqPublisherConnector(
                SOCKET_LOCAL_BASE_ADDRESS + PING_PORT
            )
            return game_cycle_connector, publisher_connector

        game_cycle_connector = ZmqReqRepConnector(
            SOCKET_STATION_ADDRESS + GAME_CYCLE_PORT
        )
        publisher_connector = ZmqPublisherConnector(SOCKET_STATION_ADDRESS + PING_PORT)
        return game_cycle_connector, publisher_connector

    def run(self):
        self.application_server.run()

    def _create_stage_service(self):
        stage_selector = self._create_stage_handler_selector()

        return StageService(stage_selector)

    def _create_stage_handler_selector(self):
        go_to_ohmmeter_handler = GoToOhmmeterHandler(
            self._communication_service,
            self._movement_service,
            ResistanceService(),
        )
        find_command_panel_handler = FindCommandPanelHandler()
        transport_puck_handler = TransportPuckHandler()
        go_park_handler = GoParkHandler()
        stop_handler = StopHandler()

        return StageHandlerSelector(
            go_to_ohmmeter_handler,
            find_command_panel_handler,
            transport_puck_handler,
            go_park_handler,
            stop_handler,
        )

    def _create_vision_service(self):
        maestro = self._create_servo_controller()
        self._configure_maestro_channel(maestro, HORIZONTAL_SERVO_ID)
        self._configure_maestro_channel(maestro, VERTICAL_SERVO_ID)

        embedded_camera = MaestroEmbeddedCamera(
            maestro,
            HORIZONTAL_SERVO_ID,
            VERTICAL_SERVO_ID,
            HORIZONTAL_ANGLE_RANGE,
            VERTICAL_ANGLE_RANGE,
        )
        letter_position_detector = PytesseractLetterPositionExtractor()

        return VisionService(embedded_camera, letter_position_detector)

    def _create_servo_controller(self):
        if self._local_flag:
            return IServoController()

        return MaestroController(ttyStr=MAESTRO_POLULU_PORT_NAME)

    def _configure_maestro_channel(self, maestro, channel_id):
        maestro.setSpeed(channel_id, SERVO_SPEED)
        maestro.setAccel(channel_id, SERVO_ACCELERATION)
