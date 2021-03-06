import time

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.communication.Message import Message
from domain.game.Topic import Topic
from domain.vision.exception.RobotNotFoundException import RobotNotFoundException
from infra.utils.GeometryUtils import GeometryUtils
from service.communication.CommunicationService import CommunicationService
from service.vision.VisionService import VisionService


class RotationService:
    def __init__(
        self, vision_service: VisionService, communication_service: CommunicationService
    ):
        self._vision_service = vision_service
        self._communication_service = communication_service

    def rotate(self, desired_orientation: Orientation):
        while True:
            time.sleep(0.5)
            robot_pose = None
            try:
                _, robot_pose = self._vision_service.get_vision_state()
            except RobotNotFoundException:
                continue
            orientation_to_send = (
                robot_pose.get_orientation_in_degree() - desired_orientation
            )
            if abs(orientation_to_send.get_orientation_in_degree()) <= 1:
                break
            orientation_to_send = self._find_smallest_orientation_to_send(
                orientation_to_send
            )
            if abs(orientation_to_send.get_orientation_in_degree()) <= 5:
                orientation_to_send = self._shrink_rotation(orientation_to_send)

            self._communication_service.send_object(
                Message(Topic.ROTATION, orientation_to_send)
            )
            message: Message = self._communication_service.receive_object()
            if (
                message.get_topic() == Topic.ROTATION_COMPLETED
                and self._is_correctly_oriented(desired_orientation)
            ):
                break

    def find_orientation_to_puck(self, puck_position: Position, robot_pose: RobotPose):
        orientation_to_puck = GeometryUtils.calculate_angle_between_positions(
            robot_pose.get_position(), puck_position
        )

        return orientation_to_puck

    def _is_correctly_oriented(self, desired_orientation: Orientation) -> bool:
        _, robot_pose = self._vision_service.get_vision_state()
        return (
            robot_pose.get_orientation_in_degree() - desired_orientation
        ) == Orientation(0)

    def _find_smallest_orientation_to_send(self, orientation_delta: Orientation):
        if orientation_delta.get_orientation_in_degree() < -180:
            return Orientation(orientation_delta.get_orientation_in_degree() + 360)
        if orientation_delta.get_orientation_in_degree() >= 180:
            return Orientation(orientation_delta.get_orientation_in_degree() - 360)

        return orientation_delta

    def _shrink_rotation(self, orientation_delta: Orientation):
        return (
            Orientation(-1)
            if orientation_delta.get_orientation_in_degree() < 0
            else Orientation(1)
        )
