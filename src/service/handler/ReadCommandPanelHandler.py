from typing import List

from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.communication.Message import Message
from domain.game.GameState import GameState
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Movement import Movement
from domain.movement.MovementFactory import MovementFactory
from service.communication.CommunicationService import CommunicationService
from service.path.PathService import PathService
from service.rotation.RotationService import RotationService


class FindCommandPanelHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        path_service: PathService,
        rotation_service: RotationService,
        movement_factory: MovementFactory,
    ):
        self._communication_service = communication_service
        self._path_service = path_service
        self._rotation_service = rotation_service
        self._movement_factory = movement_factory

    def execute(self):
        self._start_stage()
        self._go_to_puck_zone()
        self._analyze_command_panel()
        self._end_stage()

    def _start_stage(self):
        GameState.get_instance().set_current_stage(Stage.READ_COMMAND_PANEL)
        self._send_command_to_robot(Topic.START_CYCLE, Stage.READ_COMMAND_PANEL)
        self._wait_for_robot_confirmation(Topic.START_CYCLE)

    def _rotate_robot(self, wanted_orientation: Orientation):
        self._rotation_service.rotate(wanted_orientation)

    def _go_to_puck_zone(self):
        self._rotation_service.rotate(CardinalOrientation.WEST.value)
        robot_pose = GameState.get_instance().get_robot_pose()
        movements_to_puck_zone = self._find_movements_to_puck_zone(robot_pose)
        self._move_robot(movements_to_puck_zone)

    def _find_movements_to_puck_zone(self, robot_pose: RobotPose):
        path = self._path_service.find_path_to_puck_zone_center(
            robot_pose.get_position()
        )
        GameState.get_instance().set_current_planned_trajectory(path)

        return self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def _move_robot(self, movements_to_starting_zone: List[Movement]):
        self._send_command_to_robot(Topic.MOVEMENTS, movements_to_starting_zone)
        self._wait_for_robot_confirmation(Topic.MOVEMENTS)

    def _analyze_command_panel(self):
        resistance = GameState.get_instance().get_resistance_value()
        self._send_command_to_robot(Topic.ANALYZE_COMMAND_PANEL, resistance)
        read_corner = self._wait_for_robot_confirmation(Topic.ANALYZE_COMMAND_PANEL)

        next_corner = StartingZoneCorner.value_of_string(read_corner)
        corners = [next_corner]
        for _ in range(2):
            next_corner = StartingZoneCorner.get_next_corner(next_corner)
            corners.append(next_corner)

        GameState.get_instance().set_starting_zone_corners(corners)

    def _send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            try:
                return robot_response.get_payload()
            except:
                return
        else:
            print("Wrong command whoops !")

    def _end_stage(self):
        self._send_command_to_robot(Topic.STAGE_COMPLETED, None)
        self._wait_for_robot_confirmation(Topic.STAGE_COMPLETED)
