from typing import List

from domain.CardinalOrientation import CardinalOrientation
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


class StopHandler(IStageHandler):
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
        GameState.get_instance().set_current_stage(Stage.STOP)

        self._start_stage()
        self._move_to_starting_zone_center()
        self._rotation_service.rotate(CardinalOrientation.WEST.value)
        self._turn_on_led()

        self._send_command_to_robot(Topic.STAGE_COMPLETED, None)
        self._wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

        GameState.get_instance().end_game_cycle()

    def _move_to_starting_zone_center(self):
        robot_pose = GameState.get_instance().get_robot_pose()

        path = self._path_service.find_path_to_starting_zone_center(
            robot_pose.get_position()
        )
        GameState.get_instance().set_current_planned_trajectory(path)

        movements = self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

        self._move_robot(movements)

    def _turn_on_led(self):
        self._send_command_to_robot(Topic.TURN_LED_ON, None)
        self._wait_for_robot_confirmation(Topic.TURN_LED_ON)

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
            return
        else:
            print("Wrong command whoops !")

    def _start_stage(self):
        self._send_command_to_robot(Topic.START_STAGE, Stage.STOP)
        self._wait_for_robot_confirmation(Topic.START_CYCLE)
