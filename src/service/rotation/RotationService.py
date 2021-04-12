from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.communication.Message import Message
from domain.game.Topic import Topic
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
            _, robot_pose = self._vision_service.get_vision_state()
            orientation_to_send = (
                robot_pose.get_orientation_in_degree() - desired_orientation
            )
            if orientation_to_send.get_orientation_in_degree() == 0:
                break
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

        return orientation_to_puck - robot_pose.get_orientation_in_degree()

    def _is_correctly_oriented(self, desired_orientation: Orientation) -> bool:
        _, robot_pose = self._vision_service.get_vision_state()
        return (
            robot_pose.get_orientation_in_degree() - desired_orientation
        ) == Orientation(0)
