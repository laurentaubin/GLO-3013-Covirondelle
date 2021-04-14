from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.UnitOfMeasure import UnitOfMeasure
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.Color import Color
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement

from domain.movement.MovementFactory import MovementFactory
from integration.IntegrationContext import IntegrationContext
from integration.RotateTowardsPuckIT import RotateTowardsPuckIT

PUCK_COLOR_TO_USE = Color.YELLOW
STARTING_ZONE_CORNER_TO_USE = StartingZoneCorner.B


DETECT_PUCK_FOR_REAL = True
DETECT_ROBOT_FOR_REAL = True
FIND_MOVEMENTS_FOR_REAL = True


class GrabPuckIT(IntegrationContext):
    def __init__(self):
        super().__init__(local_flag=False)
        self.rotate_towards_puck_it = RotateTowardsPuckIT()

    def send_transport_puck_command(self):
        message = Message(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)
        self._communication_service.send_object(message)

    def receive_stage_started_command(self):
        message = self._communication_service.receive_game_cycle_request()
        if message.get_topic() == Topic.START_CYCLE:
            return
        else:
            print("Whoops wrong command !")

    def find_movements_to_goal(self, robot_pose: RobotPose, goal_position):
        if FIND_MOVEMENTS_FOR_REAL:
            path = self._path_service.find_path(
                robot_pose.get_position() + Position(140, 0),
                goal_position,
            )

            return MovementFactory().create_movements(
                path, robot_pose.get_orientation_in_degree()
            )
        else:
            # TODO return hardcoded movements
            pass

    def send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def find_robot_pose(self):
        if DETECT_ROBOT_FOR_REAL:
            _, robot_pose = self._vision_service.get_vision_state()
            return robot_pose
        else:
            # TODO return hardcoded position
            pass

    def find_puck_position(self, color: Color):
        if DETECT_PUCK_FOR_REAL:
            return self._path_service._game_table.get_puck(color).get_position()
        else:
            # TODO return hardcoded puck
            pass

    def wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            return
        else:
            print("Wrong command whoops !")

    def find_robot_orientation(self):
        if DETECT_ROBOT_FOR_REAL:
            _, robot_pose = self._vision_service.get_vision_state()
            return robot_pose.get_orientation_in_degree()
        else:
            # TODO return hardcoded position
            pass

    def rotate_robot(self, wanted_orientation: Orientation):
        self._rotation_service.rotate(wanted_orientation)

    def find_movements_to_starting_zone(self, robot_pose):
        path = self._path_service.find_path_to_starting_zone_center(
            robot_pose.get_position()
        )
        return MovementFactory().create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def find_movements_to_puck_zone(self, robot_pose: RobotPose):
        path = self._path_service.find_path_to_puck_zone_center(
            robot_pose.get_position()
        )

        return MovementFactory().create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def find_orientation_to_puck(self, puck_position, robot_pose):
        return self._rotation_service.find_orientation_to_puck(
            puck_position, robot_pose
        )

    def run(self):
        print("Sending start command")
        grab_puck_it.send_command_to_robot(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)
        grab_puck_it.wait_for_robot_confirmation(Topic.START_CYCLE)

        print("Rotating robot")
        grab_puck_it._rotation_service.rotate(CardinalOrientation.WEST.value)

        print("Finding robot position")
        initial_robot_pose = grab_puck_it.find_robot_pose()

        print("Finding movements to puck zone")
        movements_to_puck_zone = grab_puck_it.find_movements_to_puck_zone(
            initial_robot_pose
        )

        print("Sending movements to robot")
        grab_puck_it.send_command_to_robot(Topic.MOVEMENTS, movements_to_puck_zone)

        print("Waiting for robot to move")
        grab_puck_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

        print("Finding puck position")
        current_puck_position = grab_puck_it.find_puck_position(PUCK_COLOR_TO_USE)
        print(current_puck_position)

        self.rotate_towards_puck_it.run()

        print("Finding robot position")
        grab_puck_it.find_robot_pose()
        dropping_puck_robot_pose = grab_puck_it.find_robot_pose()

        print("Finding movements to starting zone center")
        movements_to_starting_zone = grab_puck_it.find_movements_to_starting_zone(
            dropping_puck_robot_pose
        )

        print("Sending movements to robot")
        grab_puck_it.send_command_to_robot(Topic.MOVEMENTS, movements_to_starting_zone)

        print("Waiting for robot to move")
        grab_puck_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

        print("Rotating robot towards starting zone center")
        starting_zone_corner_orientation = STARTING_ZONE_CORNER_TO_USE.value
        grab_puck_it.rotate_robot(starting_zone_corner_orientation)

        print("Sending command to drop puck")
        grab_puck_it.send_command_to_robot(Topic.DROP_PUCK, None)

        print("Waiting for robot to drop puck")
        grab_puck_it.wait_for_robot_confirmation(Topic.DROP_PUCK)

        print("Wrapping up stage")
        grab_puck_it.send_command_to_robot(Topic.STAGE_COMPLETED, None)
        grab_puck_it.wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

        print("Stage complete")


if __name__ == "__main__":
    grab_puck_it = GrabPuckIT()
    grab_puck_it.run()
