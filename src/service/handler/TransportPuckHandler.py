import time

from domain.alignment.CornerAlignmentCorrector import CornerAlignmentCorrector
from domain.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.Color import Color
from service.communication.CommunicationService import CommunicationService
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class TransportPuckHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        vision_service: VisionService,
        movement_service: MovementService,
        puck_alignment_corrector: PuckAlignmentCorrector,
        starting_zone_corner_corrector: CornerAlignmentCorrector,
    ):
        self._communication_service: CommunicationService = communication_service
        self._vision_service: VisionService = vision_service
        self._movement_service: MovementService = movement_service
        self._puck_alignment_corrector: PuckAlignmentCorrector = (
            puck_alignment_corrector
        )
        self._starting_zone_corner_corrector = starting_zone_corner_corrector

    def execute(self) -> None:
        self._communication_service.send_game_cycle_message(Stage.STAGE_STARTED)

        pucks_to_transport = self._communication_service.receive_object()

        for pucks_to_transport in pucks_to_transport:
            # TODO Receive movements to puck
            # TODO Send arrived in front of puck

            self._align_with_puck(pucks_to_transport)

            # TODO Grab puck
            # TODO Send puck grabbed
            # TODO Receive movements to corner
            # TODO Go to corner
            # TODO Align with corner
            # TODO Release puck
            # TODO Send puck dropped

    def _align_with_puck(self, puck_color: Color) -> None:
        self._correct_horizontal_alignment(puck_color)
        self._correct_vertical_alignment(puck_color)

    def _correct_horizontal_alignment(self, puck_color: Color) -> None:
        current_image = self._vision_service.take_image()
        horizontal_movement_command = (
            self._puck_alignment_corrector.calculate_horizontal_correction(
                current_image, puck_color
            )
        )
        if horizontal_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_horizontally(horizontal_movement_command, puck_color)

    def _align_horizontally(
        self, horizontal_movement_command: MovementCommand, puck_color: Color
    ) -> None:
        self._movement_service.execute_movement_command(horizontal_movement_command)
        while True:
            time.sleep(0.5)
            current_image = self._vision_service.take_image()
            horizontal_movement_command = (
                self._puck_alignment_corrector.calculate_horizontal_correction(
                    current_image, puck_color
                )
            )
            if horizontal_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    horizontal_movement_command
                )
                break

    def _correct_vertical_alignment(self, puck_color: Color) -> None:
        current_image = self._vision_service.take_image()
        vertical_movement_command = (
            self._puck_alignment_corrector.calculate_vertical_correction(
                current_image, puck_color
            )
        )
        if vertical_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_vertically(vertical_movement_command, puck_color)

    def _align_vertically(
        self, vertical_movement_command: MovementCommand, puck_color: Color
    ):
        self._movement_service.execute_movement_command(vertical_movement_command)
        while True:
            time.sleep(0.5)
            current_image = self._vision_service.take_image()
            vertical_movement_command = (
                self._puck_alignment_corrector.calculate_vertical_correction(
                    current_image, puck_color
                )
            )
            if vertical_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    vertical_movement_command
                )
                break

    def _align_with_starting_zone_corner(self) -> None:
        self._correct_horizontal_alignment_with_corner()
        self._correct_vertical_alignment_with_corner()

    def _correct_horizontal_alignment_with_corner(self) -> None:
        current_image = self._vision_service.take_image()
        horizontal_movement_command = (
            self._starting_zone_corner_corrector.calculate_horizontal_correction(
                current_image
            )
        )
        if horizontal_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_horizontally_with_corner(horizontal_movement_command)

    def _align_horizontally_with_corner(
        self, horizontal_movement_command: MovementCommand
    ) -> None:
        self._movement_service.execute_movement_command(horizontal_movement_command)
        while True:
            time.sleep(0.5)
            current_image = self._vision_service.take_image()
            horizontal_movement_command = (
                self._starting_zone_corner_corrector.calculate_horizontal_correction(
                    current_image
                )
            )
            if horizontal_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    horizontal_movement_command
                )
                break

    def _correct_vertical_alignment_with_corner(self) -> None:
        current_image = self._vision_service.take_image()
        vertical_movement_command = (
            self._starting_zone_corner_corrector.calculate_vertical_correction(
                current_image
            )
        )
        if vertical_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_vertically_with_corner(vertical_movement_command)

    def _align_vertically_with_corner(self, vertical_movement_command: MovementCommand):
        self._movement_service.execute_movement_command(vertical_movement_command)
        while True:
            time.sleep(0.5)
            current_image = self._vision_service.take_image()
            vertical_movement_command = (
                self._starting_zone_corner_corrector.calculate_vertical_correction(
                    current_image
                )
            )
            if vertical_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    vertical_movement_command
                )
                break
