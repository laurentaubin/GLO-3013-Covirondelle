from typing import List

from config.config import STARTING_ZONE_CENTER_POSITION
from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.UnitOfMeasure import UnitOfMeasure
from domain.communication.Message import Message
from domain.game.GameState import GameState
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementFactory import MovementFactory
from service.communication.CommunicationService import CommunicationService
from service.path.PathService import PathService
from service.rotation.RotationService import RotationService


class GoToOhmmeterHandler(IStageHandler):
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
        self._rotate_towards_table()
        self._go_to_starting_zone_line()
        self._rotate_resistance_reader()
        self._read_resistance()
        self._go_to_starting_zone_center()
        self._end_stage()

    def _start_stage(self):
        GameState.get_instance().set_current_stage(Stage.GO_TO_OHMMETER)
        self._send_command_to_robot(Topic.START_STAGE, Stage.GO_TO_OHMMETER)
        self._wait_for_robot_confirmation(Topic.START_STAGE)

    def _move_robot(self, movements: List[Movement]):
        command = Message(Topic.MOVEMENTS, movements)
        self._communication_service.send_object(command)
        self._wait_for_robot_confirmation(Topic.MOVEMENTS)

    def _send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            try:
                return robot_response.get_payload()
            except:
                pass
        else:
            print("Wrong command whoops !")

    def _rotate_resistance_reader(self):
        self._rotation_service.rotate(CardinalOrientation.SOUTH.value)

    def _rotate_robot(self, wanted_orientation: Orientation):
        self._rotation_service.rotate(wanted_orientation)

    def _go_to_starting_zone_line(self):
        robot_pose = RobotPose(
            Position(
                STARTING_ZONE_CENTER_POSITION[0], STARTING_ZONE_CENTER_POSITION[0]
            ),
            Orientation(CardinalOrientation.WEST.value),
        )
        path = self._path_service.find_path_to_ohmmeter(robot_pose.get_position())
        GameState.get_instance().set_current_planned_trajectory(path)

        movements = self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )
        self._move_robot(movements)

    def _read_resistance(self):
        self._send_command_to_robot(Topic.READ_RESISTANCE, None)
        resistance = self._wait_for_robot_confirmation(Topic.READ_RESISTANCE)
        GameState.get_instance().set_resistance_value(resistance)

    def _end_stage(self):
        self._send_command_to_robot(Topic.STAGE_COMPLETED, None)
        self._wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

    def _rotate_towards_table(self):
        self._rotate_robot(CardinalOrientation.EAST.value)

    def _go_to_starting_zone_center(self):
        # TODO Maybe get this out of here to now look clanky at the beginning of the stage
        movements_to_starting_zone = [
            Movement(
                Direction.FORWARD, Distance(0.45, unit_of_measure=UnitOfMeasure.METER)
            ),
            Movement(
                Direction.RIGHT, Distance(0.35, unit_of_measure=UnitOfMeasure.METER)
            ),
        ]
        self._move_robot(movements_to_starting_zone)

    def _find_movements_to_puck_zone(self, robot_pose: RobotPose):
        path = self._path_service.find_path_to_starting_zone_center(
            robot_pose.get_position()
        )
        GameState.get_instance().set_current_planned_trajectory(path)

        return self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )
