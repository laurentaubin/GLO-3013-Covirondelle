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
)
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.MovementFactory import MovementFactory
from infra.communication.motor_controller.FakeMotorController import FakeMotorController
from infra.communication.motor_controller.StmMotorController import StmMotorController
from infra.communication.station.ZmqPublisherConnector import ZmqPublisherConnector
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector
from infra.game.SlaveGameCycle import SlaveGameCycle
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


class RobotContext:
    def __init__(self, local_flag):
        self._local_flag = local_flag

        game_cycle_connector, pub_sub_connector = self._create_connectors()

        self.communication_service = CommunicationService(
            game_cycle_connector, pub_sub_connector
        )
        movement_command_factory = MovementCommandFactory(
            ROBOT_MAXIMUM_SPEED,
            SERVOING_CONSTANT,
            BASE_COMMAND_DURATION,
        )
        motor_controller = self._create_motor_controller(movement_command_factory)

        movement_factory = MovementFactory()
        self.movement_service = MovementService(movement_factory, motor_controller)

        self.stage_service = self._create_stage_service()
        self.slave_game_cycle = SlaveGameCycle(
            self.communication_service, self.stage_service
        )

        self.communication_runner = CommunicationRunner(self.communication_service)

        self.application_server = ApplicationServer(
            self.communication_runner, self.slave_game_cycle
        )

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

        return StageHandlerSelector(
            go_to_ohmmeter_handler,
            find_command_panel_handler,
            transport_puck_handler,
            go_park_handler,
            stop_handler,
        )
