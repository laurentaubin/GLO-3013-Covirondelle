import time
from typing import List, Any

from domain.Orientation import Orientation
from domain.alignment.CommandPanelAlignmentCorrector import (
    CommandPanelAlignmentCorrector,
)
from domain.communication.Message import Message
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.resistance.Resistance import Resistance
from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor
from service.communication.CommunicationService import CommunicationService
from service.exception.StageComplete import StageComplete
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class ReadCommandPanelHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        movement_service: MovementService,
        vision_service: VisionService,
        command_panel_alignment_corrector: CommandPanelAlignmentCorrector,
        command_panel_letters_extractor: ILetterPositionExtractor,
    ):
        self._communication_service = communication_service
        self._movement_service = movement_service
        self._vision_service = vision_service
        self._command_panel_alignment_corrector = command_panel_alignment_corrector
        self._command_panel_letters_extractor = command_panel_letters_extractor

    def execute(self):
        while True:
            try:
                self._route_station_command()
            except StageComplete:
                break

    def _route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()

        if (
            topic == Topic.START_STAGE
            and command.get_payload() == Stage.READ_COMMAND_PANEL
        ):
            self._send_confirmation_to_station(
                Topic.START_STAGE, Stage.READ_COMMAND_PANEL
            )

        elif topic == Topic.MOVEMENTS:
            self._move(command.get_payload())
            self._send_confirmation_to_station(Topic.MOVEMENTS, Stage.STAGE_COMPLETED)

        elif topic == Topic.ROTATION:
            self._rotate(command.get_payload())
            self._send_confirmation_to_station(Topic.ROTATION, Stage.STAGE_COMPLETED)

        elif topic == Topic.ANALYZE_COMMAND_PANEL:
            first_starting_zone_line_corner = self._read_command_panel(
                command.get_payload()
            )
            self._send_confirmation_to_station(
                Topic.ANALYZE_COMMAND_PANEL, first_starting_zone_line_corner
            )

        elif topic == Topic.STAGE_COMPLETED:
            self._send_confirmation_to_station(
                Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
            )
            raise StageComplete

    def _send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _rotate(self, orientation: Orientation):
        self._movement_service.rotate(orientation.get_orientation_in_degree())

    def _move(self, movements: List[Movement]):
        self._movement_service.move(movements)

    def _read_command_panel(self, resistance: Resistance):
        self._vision_service.make_camera_look_up()
        self._align_horizontally_with_command_panel()
        self._vision_service.take_image()
        current_image = self._vision_service.take_image()
        command_panel_letters = (
            self._command_panel_letters_extractor.extract_letters_from_image(
                current_image
            )
        )

        letter_position = resistance.find_nth_digit(0) - 1
        return command_panel_letters[letter_position]

    def _align_horizontally_with_command_panel(self):
        self._move_to_the_left()
        time.sleep(0.5)
        current_image = self._vision_service.take_image()
        horizontal_movement = (
            self._command_panel_alignment_corrector.calculate_horizontal_correction(
                current_image
            )
        )
        if horizontal_movement.get_direction() == Direction.STOP:
            return
        else:
            self._correct_horizontal_position()

    def _correct_horizontal_position(self):
        self._move_to_the_right_until_can_read_all_nine_letters()

    def _move_to_the_right(self):
        self._movement_service.move([Movement(Direction.RIGHT, Distance(0.10))])

    def _move_to_the_left(self):
        self._movement_service.move([Movement(Direction.LEFT, Distance(0.20))])

    def _move_to_the_right_until_can_read_all_nine_letters(self):
        while True:
            current_image = self._vision_service.take_image()
            horizontal_movement = (
                self._command_panel_alignment_corrector.calculate_horizontal_correction(
                    current_image
                )
            )
            if horizontal_movement.get_direction() == Direction.STOP:
                break

            self._movement_service.move([horizontal_movement])
