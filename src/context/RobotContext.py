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
    CAMERA_HORIZONTAL_SERVO_ID,
    CAMERA_VERTICAL_SERVO_ID,
    SERVO_SPEED,
    SERVO_ACCELERATION,
    HORIZONTAL_ANGLE_RANGE,
    VERTICAL_ANGLE_RANGE,
    MAESTRO_POLULU_PORT_NAME,
    GRIPPER_HORIZONTAL_SERVO_ID,
    GRIPPER_VERTICAL_SERVO_ID,
    OPEN_GRIPPER_TARGET,
    CLOSE_GRIPPER_TARGET,
    MOVE_GRIPPER_UP_TARGET,
    MOVE_GRIPPER_DOWN_TARGET,
    PUCK_ALIGNMENT_X_CENTER_POSITION,
    PUCK_ALIGNMENT_Y_CENTER_POSITION,
    PUCK_ALIGNMENT_THRESHOLD,
    CAMERA_INDEX,
    ROBOT_ROTATION_SPEED,
    ROBOT_RADIUS,
)
from domain.Position import Position
from domain.communication.IRobotInformation import IRobotInformation
from domain.movement.CommandDuration import CommandDuration
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed
from domain.vision.IPuckDetector import IPuckDetector
from infra.IServoController import IServoController
from infra.MaestroController import MaestroController
from domain.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera
from infra.communication.robot_information.StmRobotInformation import (
    StmRobotInformation,
)

from infra.communication.station.ZmqPublisherConnector import ZmqPublisherConnector
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector
from infra.game.SlaveGameCycle import SlaveGameCycle
from infra.gripper.MaestroGripper import MaestroGripper
from infra.motor_controller.FakeMotorController import FakeMotorController
from infra.motor_controller.StmMotorController import StmMotorController
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)
from service.communication.CommunicationService import CommunicationService
from service.game.StageHandlerSelector import StageHandlerSelector
from service.game.StageService import StageService
from service.gripper.GripperService import GripperService
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

        if not self._local_flag:
            self._serial = serial.Serial(port=STM_PORT_NAME, baudrate=STM_BAUD_RATE)

        self._communication_service = self._create_communication_service()
        self._movement_service = self._create_movement_service()
        self._maestro = self._create_and_configure_maestro()
        self._vision_service = self._create_vision_service()
        self._gripper_service = self._create_gripper_service()

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
        robot_information = self._create_robot_information()
        return CommunicationService(
            game_cycle_connector, pub_sub_connector, robot_information
        )

    def _create_robot_information(self):
        if self._local_flag:
            return IRobotInformation()
        return StmRobotInformation(self._serial)

    def _create_movement_service(self):
        movement_command_factory = MovementCommandFactory(
            Speed(ROBOT_MAXIMUM_SPEED),
            Speed(SERVOING_CONSTANT),
            CommandDuration(BASE_COMMAND_DURATION),
            Speed(ROBOT_ROTATION_SPEED),
            ROBOT_RADIUS,
        )
        motor_controller = self._create_motor_controller()
        return MovementService(movement_command_factory, motor_controller)

    def _create_motor_controller(self):
        if self._local_flag:
            return FakeMotorController()

        return StmMotorController(
            self._serial,
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
        puck_alignment_corrector = self._create_puck_alignment_corrector(
            OpenCvPuckDetector()
        )
        transport_puck_handler = TransportPuckHandler(
            self._communication_service,
            self._vision_service,
            self._movement_service,
            puck_alignment_corrector,
        )
        go_park_handler = GoParkHandler()
        stop_handler = StopHandler()

        return StageHandlerSelector(
            go_to_ohmmeter_handler,
            find_command_panel_handler,
            transport_puck_handler,
            go_park_handler,
            stop_handler,
        )

    def _create_and_configure_maestro(self):
        maestro = self._create_servo_controller()
        self._configure_maestro_channel(maestro, GRIPPER_HORIZONTAL_SERVO_ID)
        self._configure_maestro_channel(maestro, GRIPPER_VERTICAL_SERVO_ID)
        self._configure_maestro_channel(maestro, CAMERA_HORIZONTAL_SERVO_ID)
        self._configure_maestro_channel(maestro, CAMERA_VERTICAL_SERVO_ID)

        return maestro

    def _create_vision_service(self):

        embedded_camera = OpenCvEmbeddedCamera(
            CAMERA_INDEX,
            self._maestro,
            CAMERA_HORIZONTAL_SERVO_ID,
            CAMERA_VERTICAL_SERVO_ID,
            HORIZONTAL_ANGLE_RANGE,
            VERTICAL_ANGLE_RANGE,
        )
        letter_position_detector = PytesseractLetterPositionExtractor()

        return VisionService(embedded_camera, letter_position_detector)

    def _create_gripper_service(self):
        gripper = MaestroGripper(
            self._maestro,
            GRIPPER_HORIZONTAL_SERVO_ID,
            GRIPPER_VERTICAL_SERVO_ID,
            OPEN_GRIPPER_TARGET,
            CLOSE_GRIPPER_TARGET,
            MOVE_GRIPPER_UP_TARGET,
            MOVE_GRIPPER_DOWN_TARGET,
        )

        return GripperService(gripper)

    def _create_servo_controller(self):
        if self._local_flag:
            return IServoController()

        return MaestroController(ttyStr=MAESTRO_POLULU_PORT_NAME)

    def _configure_maestro_channel(self, maestro, channel_id):
        maestro.setSpeed(channel_id, SERVO_SPEED)
        maestro.setAccel(channel_id, SERVO_ACCELERATION)

    def _create_puck_alignment_corrector(
        self, puck_detector: IPuckDetector
    ) -> PuckAlignmentCorrector:
        puck_center_position = Position(
            PUCK_ALIGNMENT_X_CENTER_POSITION, PUCK_ALIGNMENT_Y_CENTER_POSITION
        )
        return PuckAlignmentCorrector(
            puck_center_position, PUCK_ALIGNMENT_THRESHOLD, puck_detector
        )
