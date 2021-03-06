from unittest.mock import MagicMock

from application.ApplicationServer import ApplicationServer
from application.CommunicationRunner import CommunicationRunner
from config.config import (
    PING_PORT,
    GAME_CYCLE_PORT,
    STM_PORT_NAME,
    STM_BAUD_RATE,
    ROBOT_MAXIMUM_SPEED,
    SERVOING_CONSTANT,
    BASE_COMMAND_DURATION,
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
    CAMERA_INDEX,
    ALIGNED_OHMMETER_HORIZONTAL_POSITION,
    OHMMETER_ALIGNMENT_THRESHOLD,
    RESISTANCE_READ_THRESHOLD,
    AN_IMAGE_PATH,
    PUCK_ALIGNMENT_HORIZONTAL_THRESHOLD,
    CAMERA_LOOK_UP_TARGET,
    CAMERA_LOOK_DOWN_TARGET,
    STARTING_ZONE_CORNER_POSITION,
    NUMBER_OF_LETTERS_TO_READ,
    COMMAND_PANEL_VERTICAL_POSITION,
    COMMAND_PANEL_HORIZONTAL_POSITION,
    PUCK_ALIGNMENT_UP_THRESHOLD,
    SOCKET_LOCAL_BASE_ADDRESS,
    SOCKET_STATION_ADDRESS,
    SOCKET_ANY_ADDRESS,
)
from domain.Position import Position
from domain.alignment.CommandPanelAlignmentCorrector import (
    CommandPanelAlignmentCorrector,
)
from domain.alignment.CornerAlignmentCorrector import CornerAlignmentCorrector
from domain.alignment.OhmmeterAlignmentCorrector import OhmmeterAlignmentCorrector
from domain.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from domain.movement.CommandDuration import CommandDuration
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed
from domain.resistance.IOhmmeter import IOhmmeter
from domain.vision.IStartingZoneLineDetector import IStartingZoneLineDetector
from infra.IServoController import IServoController
from infra.MaestroController import MaestroController
from infra.camera.ImageBasedEmbeddedCamera import ImageBasedEmbeddedCamera
from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera
from infra.communication.ThreadSafeSerial import ThreadSafeSerial
from infra.communication.robot_information.FakeRobotInformation import (
    FakeRobotInformation,
)
from infra.communication.robot_information.StmLed import StmLed
from infra.communication.robot_information.StmRobotInformation import (
    StmRobotInformation,
)
from infra.communication.station.ZmqPublisherConnector import ZmqPublisherConnector
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector
from infra.game.SlaveGameCycle import SlaveGameCycle
from infra.gripper.MaestroGripper import MaestroGripper
from infra.motor_controller.FakeMotorController import FakeMotorController
from infra.motor_controller.StmMotorController import StmMotorController
from infra.resistance.StmOhmmeter import StmOhmmeter
from infra.vision.OpenCvCommandPanelDetector import OpenCvCommandPanelDetector
from infra.vision.OpenCvCornerDetector import OpenCvCornerDetector
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector
from infra.vision.OpenCvStartingZoneLineDetector import OpenCvStartingZoneLineDetector
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)
from infra.vision.TemplateMatchingPuckDetector import TemplateMatchingPuckDetector
from service.communication.CommunicationService import CommunicationService
from service.game.StageHandlerSelector import StageHandlerSelector
from service.game.StageService import StageService
from service.gripper.GripperService import GripperService
from service.handler.ReadCommandPanelHandler import ReadCommandPanelHandler
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler
from service.handler.StartHandler import StartHandler
from service.handler.StopHandler import StopHandler
from service.handler.TransportPuckHandler import TransportPuckHandler
from service.movement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService
from service.vision.VisionService import VisionService


class RobotContext:
    ANY_VERTICAL_POSITION = 0

    def __init__(self, local_flag):
        self._local_flag = local_flag

        if not self._local_flag:
            self._serial = ThreadSafeSerial(STM_PORT_NAME, STM_BAUD_RATE)
        else:
            self._serial = MagicMock()

        self._led = StmLed(self._serial)

        movement_command_factory = MovementCommandFactory(
            Speed(ROBOT_MAXIMUM_SPEED),
            Speed(SERVOING_CONSTANT),
            CommandDuration(BASE_COMMAND_DURATION),
        )

        self._communication_service = self._create_communication_service()
        self._movement_service = self._create_movement_service(movement_command_factory)
        self._maestro = self._create_and_configure_maestro()
        self._vision_service = self._create_vision_service()
        self._gripper_service = self._create_gripper_service()
        self._resistance_service = self._create_resistance_service()

        self.stage_service = self._create_stage_service(movement_command_factory)
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
            return FakeRobotInformation()
        return StmRobotInformation(self._serial)

    def _create_movement_service(
        self, movement_command_factory: MovementCommandFactory
    ):
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
                SOCKET_ANY_ADDRESS + GAME_CYCLE_PORT
            )
            publisher_connector = ZmqPublisherConnector(
                SOCKET_LOCAL_BASE_ADDRESS + PING_PORT
            )
            return game_cycle_connector, publisher_connector

        game_cycle_connector = ZmqReqRepConnector(SOCKET_ANY_ADDRESS + GAME_CYCLE_PORT)
        publisher_connector = ZmqPublisherConnector(SOCKET_STATION_ADDRESS + PING_PORT)
        return game_cycle_connector, publisher_connector

    def run(self):
        self.application_server.run()

    def _create_stage_service(self, movement_command_factory: MovementCommandFactory):
        stage_selector = self._create_stage_handler_selector(movement_command_factory)

        return StageService(stage_selector)

    def _create_stage_handler_selector(
        self, movement_command_factory: MovementCommandFactory
    ):
        start_handler = StartHandler(
            self._communication_service, self._gripper_service, self._led
        )
        ohmmeter_alignment_corrector = self._create_ohmmeter_alignment_corrector(
            OpenCvStartingZoneLineDetector()
        )
        go_to_ohmmeter_handler = GoToOhmmeterHandler(
            self._communication_service,
            self._movement_service,
            self._resistance_service,
            self._vision_service,
            ohmmeter_alignment_corrector,
            movement_command_factory,
        )
        panel_command_detector = OpenCvCommandPanelDetector()
        command_panel_letters_extractor = PytesseractLetterPositionExtractor()
        self.command_panel_alignment_corrector = CommandPanelAlignmentCorrector(
            NUMBER_OF_LETTERS_TO_READ,
            Position(
                COMMAND_PANEL_HORIZONTAL_POSITION, COMMAND_PANEL_VERTICAL_POSITION
            ),
            panel_command_detector,
            command_panel_letters_extractor,
        )
        self._read_command_panel_handler = ReadCommandPanelHandler(
            self._communication_service,
            self._movement_service,
            self._vision_service,
            self.command_panel_alignment_corrector,
            command_panel_letters_extractor,
        )
        self._transport_puck_handler = self._create_transport_puck_handler()
        stop_handler = StopHandler(
            self._communication_service, self._movement_service, self._led
        )

        return StageHandlerSelector(
            start_handler,
            go_to_ohmmeter_handler,
            self._read_command_panel_handler,
            self._transport_puck_handler,
            stop_handler,
        )

    def _create_transport_puck_handler(self):
        starting_zone_corner_position = Position(
            STARTING_ZONE_CORNER_POSITION[0], STARTING_ZONE_CORNER_POSITION[1]
        )
        starting_zone_corner_corrector = CornerAlignmentCorrector(
            OpenCvCornerDetector(), starting_zone_corner_position
        )
        puck_alignment_corrector = self._create_puck_alignment_corrector()
        transport_puck_handler = TransportPuckHandler(
            self._communication_service,
            self._vision_service,
            self._movement_service,
            self._gripper_service,
            puck_alignment_corrector,
            starting_zone_corner_corrector,
        )
        return transport_puck_handler

    def _create_and_configure_maestro(self):
        maestro = self._create_servo_controller()
        self._configure_maestro_channel(maestro, GRIPPER_HORIZONTAL_SERVO_ID)
        self._configure_maestro_channel(maestro, GRIPPER_VERTICAL_SERVO_ID)
        self._configure_maestro_channel(maestro, CAMERA_HORIZONTAL_SERVO_ID)
        self._configure_maestro_channel(maestro, CAMERA_VERTICAL_SERVO_ID)

        return maestro

    def _create_vision_service(self):

        embedded_camera = self._create_embedded_camera()
        letter_position_detector = PytesseractLetterPositionExtractor()

        return VisionService(
            embedded_camera,
            letter_position_detector,
            CAMERA_LOOK_DOWN_TARGET,
            CAMERA_LOOK_UP_TARGET,
        )

    def _create_embedded_camera(self):
        if self._local_flag:
            return ImageBasedEmbeddedCamera(AN_IMAGE_PATH)

        return OpenCvEmbeddedCamera(
            CAMERA_INDEX,
            self._maestro,
            CAMERA_HORIZONTAL_SERVO_ID,
            CAMERA_VERTICAL_SERVO_ID,
            HORIZONTAL_ANGLE_RANGE,
            VERTICAL_ANGLE_RANGE,
        )

    def _create_gripper_service(self):
        gripper = MaestroGripper(
            self._maestro,
            GRIPPER_HORIZONTAL_SERVO_ID,
            GRIPPER_VERTICAL_SERVO_ID,
            CLOSE_GRIPPER_TARGET,
            OPEN_GRIPPER_TARGET,
            MOVE_GRIPPER_UP_TARGET,
            MOVE_GRIPPER_DOWN_TARGET,
        )

        return GripperService(gripper)

    def _create_resistance_service(self):
        ohmmeter = self._create_ohmmeter()
        return ResistanceService(RESISTANCE_READ_THRESHOLD, ohmmeter)

    def _create_servo_controller(self):
        if self._local_flag:
            return IServoController()

        return MaestroController(ttyStr=MAESTRO_POLULU_PORT_NAME)

    def _create_ohmmeter(self):
        if self._local_flag:
            return IOhmmeter()
        return StmOhmmeter(self._serial)

    def _configure_maestro_channel(self, maestro, channel_id):
        maestro.setSpeed(channel_id, SERVO_SPEED)
        maestro.setAccel(channel_id, SERVO_ACCELERATION)

    def _create_puck_alignment_corrector(
        self,
    ) -> PuckAlignmentCorrector:
        puck_correctly_placed_position = Position(
            PUCK_ALIGNMENT_X_CENTER_POSITION, PUCK_ALIGNMENT_Y_CENTER_POSITION
        )
        return PuckAlignmentCorrector(
            puck_correctly_placed_position,
            PUCK_ALIGNMENT_HORIZONTAL_THRESHOLD,
            PUCK_ALIGNMENT_UP_THRESHOLD,
            OpenCvPuckDetector(),
            TemplateMatchingPuckDetector(),
        )

    def _create_ohmmeter_alignment_corrector(
        self, starting_zone_line_detector: IStartingZoneLineDetector
    ):
        line_position_reference = Position(
            ALIGNED_OHMMETER_HORIZONTAL_POSITION, self.ANY_VERTICAL_POSITION
        )
        return OhmmeterAlignmentCorrector(
            line_position_reference,
            OHMMETER_ALIGNMENT_THRESHOLD,
            starting_zone_line_detector,
        )
