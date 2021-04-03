import time
from typing import List

from config.config import MIN_VERTICAL_ANGLE_VALUE
from domain.alignment.OhmmeterAlignmentCorrector import OhmmeterAlignmentCorrector
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.movement.Direction import Direction
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.resistance.Resistance import Resistance
from service.communication.CommunicationService import CommunicationService
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
        self._communication_service.send_game_cycle_message(Stage.GO_TO_OHMMETER.value)

        movements: List[Movement] = self._communication_service.receive_object()
        self._movement_service.move(movements)

        self._align_with_ohmmeter()

        resistance_value: Resistance = (
            self._resistance_service.take_resistance_measurement()
        )
        self._communication_service.send_object(resistance_value)

        self._route_station_response()
        self._communication_service.send_game_cycle_message(Stage.STAGE_COMPLETED.value)

    def _route_station_response(self):
        game_cycle = self._communication_service.receive_game_cycle_message()

        if game_cycle == Stage.STAGE_COMPLETED.value:
            pass
        else:
            print("whoops")

    def _align_with_ohmmeter(self):
        self._align_horizontally_with_ohmmeter()
        self._make_contact_with_ohmmeter()

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
            time.sleep(0.5)
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
                self._movement_service.execute_movement_command(
                    self._movement_command_factory.create_stop_command()
                )
                break
