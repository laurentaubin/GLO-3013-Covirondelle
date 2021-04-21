import time
from typing import Any, List

from domain.Orientation import Orientation
from domain.alignment.CornerAlignmentCorrector import CornerAlignmentCorrector
from domain.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from domain.communication.Message import Message
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Movement import Movement
from domain.movement.MovementCommand import MovementCommand
from domain.Color import Color
from domain.vision.exception.PuckNotFoundException import PuckNotFoundException
from service.communication.CommunicationService import CommunicationService
from service.exception.StageComplete import StageComplete
from service.gripper.GripperService import GripperService
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class TransportPuckHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        vision_service: VisionService,
        movement_service: MovementService,
        gripper_service: GripperService,
        puck_alignment_corrector: PuckAlignmentCorrector,
        starting_zone_corner_corrector: CornerAlignmentCorrector,
    ):
        self._communication_service: CommunicationService = communication_service
        self._vision_service: VisionService = vision_service
        self._movement_service: MovementService = movement_service
        self._gripper_service = gripper_service
        self._puck_alignment_corrector: PuckAlignmentCorrector = (
            puck_alignment_corrector
        )
        self._starting_zone_corner_corrector = starting_zone_corner_corrector

    def execute(self) -> None:
        self._gripper_service.open_gripper()

        while True:
            try:
                self._route_station_command()
            except StageComplete:
                break

    def _route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()

        if topic == Topic.START_STAGE:
            self._send_confirmation_to_station(Topic.START_STAGE, Stage.TRANSPORT_PUCK)

        elif topic == Topic.MOVEMENTS:
            self._move(command.get_payload())
            self._send_confirmation_to_station(Topic.MOVEMENTS, Stage.STAGE_COMPLETED)

        elif topic == Topic.ROTATION:
            self._rotate(command.get_payload())
            self._send_confirmation_to_station(Topic.ROTATION, Stage.STAGE_COMPLETED)

        elif topic == Topic.GRAB_PUCK:
            self._grab_puck(Color.value_of_resistance_digit(command.get_payload()))
            self._send_confirmation_to_station(Topic.GRAB_PUCK, Stage.STAGE_COMPLETED)

        elif topic == Topic.DROP_PUCK:
            self._drop_puck()
            self._gripper_service.elevate_gripper()
            self._send_confirmation_to_station(Topic.DROP_PUCK, Stage.STAGE_COMPLETED)

        elif topic == Topic.STAGE_COMPLETED:
            self._send_confirmation_to_station(
                Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
            )
            raise StageComplete

    def _send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _grab_puck(self, puck_color: Color):
        self._vision_service.make_camera_look_down()
        time.sleep(0.2)
        self._open_gripper()
        self._align_with_puck(puck_color)
        print("Closing gripper")
        self._gripper_service.close_gripper()
        time.sleep(1)
        self._gripper_service.elevate_gripper()

    def _move(self, movements: List[Movement]):
        self._movement_service.move(movements)

    def _open_gripper(self):
        self._gripper_service.open_gripper()
        self._gripper_service.lower_gripper()

    def _drop_puck(self):
        self._align_with_starting_zone_corner()

        self._gripper_service.lower_gripper()
        time.sleep(1)
        self._gripper_service.open_gripper()

    def _rotate(self, orientation: Orientation):
        self._movement_service.rotate(orientation.get_orientation_in_degree())

    def _align_with_puck(self, puck_color: Color) -> None:
        while True:
            current_image = self._vision_service.take_image()
            movement_command = (
                self._puck_alignment_corrector.move_forward_until_puck_is_detected(
                    current_image, puck_color
                )
            )
            self._movement_service.execute_movement_command(movement_command)
            if movement_command.get_direction() == Direction.STOP:
                break
        self._correct_horizontal_alignment_with_puck(puck_color)
        self._correct_vertical_alignment(puck_color)

    def _correct_horizontal_alignment_with_puck(self, puck_color: Color) -> None:
        current_image = self._vision_service.take_image()
        horizontal_movement_command = (
            self._puck_alignment_corrector.calculate_horizontal_correction(
                current_image, puck_color
            )
        )
        if horizontal_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_horizontally_with_puck(horizontal_movement_command, puck_color)

    def _align_horizontally_with_puck(
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
            self._movement_service.execute_movement_command(horizontal_movement_command)

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
            self._align_vertically_with_puck(vertical_movement_command, puck_color)

    def _align_vertically_with_puck(
        self, vertical_movement_command: MovementCommand, puck_color: Color
    ):
        self._movement_service.execute_movement_command(vertical_movement_command)
        while True:
            try:
                time.sleep(0.5)
                current_image = self._vision_service.take_image()
                vertical_movement_command = (
                    self._puck_alignment_corrector.calculate_vertical_correction(
                        current_image, puck_color
                    )
                )
                if vertical_movement_command.get_direction() == Direction.STOP:
                    time.sleep(1.5)
                    self._movement_service.execute_movement_command(
                        vertical_movement_command
                    )
                    break
            except PuckNotFoundException:
                pass

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
            self._movement_service.execute_movement_command(horizontal_movement_command)

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
