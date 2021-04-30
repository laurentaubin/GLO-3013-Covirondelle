import time
from typing import List, Any

from config.config import MIN_VERTICAL_ANGLE_VALUE, HORIZONTAL_MIDDLE_TARGET
from domain.Orientation import Orientation
from domain.alignment.OhmmeterAlignmentCorrector import OhmmeterAlignmentCorrector
from domain.communication.Message import Message
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.MovementCommandFactory import MovementCommandFactory
from service.communication.CommunicationService import CommunicationService
from service.exception.StageComplete import StageComplete
from service.movement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService
from service.vision.VisionService import VisionService


class GoToOhmmeterHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        movement_service: MovementService,
        resistance_service: ResistanceService,
        vision_service: VisionService,
        ohmmeter_alignment_corrector: OhmmeterAlignmentCorrector,
        movement_command_factory: MovementCommandFactory,
    ):
        self._communication_service = communication_service
        self._movement_service = movement_service
        self._resistance_service = resistance_service
        self._vision_service = vision_service
        self._ohmmeter_alignment_corrector = ohmmeter_alignment_corrector
        self._movement_command_factory = movement_command_factory

    def execute(self):
        while True:
            try:
                self._route_station_command()
            except StageComplete:
                break

    def _route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()
        if topic == Topic.START_STAGE:
            self._send_confirmation_to_station(Topic.START_STAGE, Stage.GO_TO_OHMMETER)

        elif topic == Topic.MOVEMENTS:
            self._move(command.get_payload())
            self._send_confirmation_to_station(Topic.MOVEMENTS, Stage.STAGE_COMPLETED)

        elif topic == Topic.ROTATION:
            self._rotate(command.get_payload())
            self._send_confirmation_to_station(Topic.ROTATION, Stage.STAGE_COMPLETED)

        elif topic == Topic.READ_RESISTANCE:
            resistance = self._read_resistance()
            self._send_confirmation_to_station(Topic.READ_RESISTANCE, resistance)

        elif topic == Topic.STAGE_COMPLETED:
            self._send_confirmation_to_station(
                Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
            )
            raise StageComplete

    def _read_resistance(self):
        self._vision_service.make_camera_look_down()
        self._vision_service.rotate_camera_horizontally(HORIZONTAL_MIDDLE_TARGET)
        self._align_horizontally_with_ohmmeter()
        self._make_contact_with_ohmmeter()
        return self._resistance_service.take_resistance_measurement()

    def _align_horizontally_with_ohmmeter(self):
        self._vision_service.rotate_camera_vertically(MIN_VERTICAL_ANGLE_VALUE)
        # TODO wait or the camera rotation complete before going to the next instruction?
        current_image = self._vision_service.take_image()
        adjustment_movement_command = (
            self._ohmmeter_alignment_corrector.calculate_horizontal_correction(
                current_image
            )
        )
        if adjustment_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._correct_horizontal_alignment(adjustment_movement_command)

    def _correct_horizontal_alignment(self, movement_command: MovementCommand):
        self._movement_service.execute_movement_command(movement_command)
        while movement_command.get_direction() != Direction.STOP:
            current_image = self._vision_service.take_image()
            horizontal_movement_command = (
                self._ohmmeter_alignment_corrector.calculate_horizontal_correction(
                    current_image
                )
            )
            if horizontal_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    horizontal_movement_command
                )
                break
            self._movement_service.execute_movement_command(horizontal_movement_command)

    def _make_contact_with_ohmmeter(self):
        backwards_alignment_movement_command = (
            self._movement_command_factory.create_alignment_movement_command(
                Direction.BACKWARDS
            )
        )
        self._movement_service.execute_movement_command(
            backwards_alignment_movement_command
        )
        while True:
            time.sleep(0.5)
            if self._resistance_service.confirm_contact():
                time.sleep(2)
                self._movement_service.execute_movement_command(
                    self._movement_command_factory.create_stop_command()
                )
                break

    def _move(self, movements: List[Movement]):
        self._movement_service.move(movements)

    def _rotate(self, orientation: Orientation):
        self._movement_service.rotate(orientation.get_orientation_in_degree())

    def _send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)
