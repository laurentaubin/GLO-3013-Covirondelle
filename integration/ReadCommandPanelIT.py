from typing import List

from domain.CardinalOrientation import CardinalOrientation
from domain.Color import Color
from domain.StartingZoneCorner import StartingZoneCorner
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Movement import Movement
from domain.resistance.Resistance import Resistance
from integration.IntegrationContext import IntegrationContext
from integration.RotateTowardsPuckIT import RotateTowardsPuckIT

DETECT_ROBOT_FOR_REAL = True


class ReadCommandPanelIT(IntegrationContext):
    def __init__(self):
        super().__init__(local_flag=False)
        self.rotate_towards_puck_it = RotateTowardsPuckIT()

    def send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            return
        else:
            print("Wrong command whoops !")

    def _find_robot_pose(self):
        if DETECT_ROBOT_FOR_REAL:
            _, robot_pose = self._vision_service.get_vision_state()
            return robot_pose
        else:
            pass

    def _find_movements_to_starting_zone(self, robot_pose):
        path = self._path_service.find_path_to_starting_zone_center(
            robot_pose.get_position()
        )
        return self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def _move_robot(self, movements_to_starting_zone: List[Movement]):
        self.send_command_to_robot(Topic.MOVEMENTS, movements_to_starting_zone)
        self.wait_for_robot_confirmation(Topic.MOVEMENTS)

    def _receive_first_starting_zone_corner(self):
        robot_response: Message = self._communication_service.receive_object()
        if robot_response.get_topic() == Topic.ANALYZE_COMMAND_PANEL:
            return robot_response.get_payload()
        else:
            print("Did not send first starting zone corner")

    def run(self):
        print("Sending start command")
        self.send_command_to_robot(Topic.START_STAGE, Stage.READ_COMMAND_PANEL)
        self.wait_for_robot_confirmation(Topic.START_STAGE)

        print("Send movements to starting zone center")
        self._rotation_service.rotate(CardinalOrientation.SOUTH.value)
        robot_pose = self._find_robot_pose()
        movements_to_starting_zone = self._find_movements_to_starting_zone(robot_pose)
        self._move_robot(movements_to_starting_zone)

        print("Send rotation to robot to face command panel")
        self._rotation_service.rotate(CardinalOrientation.WEST.value)

        print("Send read command panel")
        self.send_command_to_robot(Topic.ANALYZE_COMMAND_PANEL, Resistance(260000))
        first_starting_zone_corner: StartingZoneCorner = (
            self._receive_first_starting_zone_corner()
        )
        print(
            "The first corner received is: {}".format(first_starting_zone_corner.name)
        )

        print("Wrapping up stage")
        self.send_command_to_robot(Topic.STAGE_COMPLETED, None)
        self.wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

        print("Stage complete")


if __name__ == "__main__":
    grab_puck_it = ReadCommandPanelIT()
    grab_puck_it.run()
