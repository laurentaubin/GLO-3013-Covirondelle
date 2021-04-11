from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.StartingZoneCorner import StartingZoneCorner
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.Color import Color
from domain.game.Topic import Topic

from domain.movement.MovementFactory import MovementFactory
from integration.IntegrationContext import IntegrationContext


PUCK_COLOR_TO_USE = Color.ORANGE
STARTING_ZONE_CORNER_TO_USE = StartingZoneCorner.B


DETECT_PUCK_FOR_REAL = True
DETECT_ROBOT_FOR_REAL = True
FIND_MOVEMENTS_FOR_REAL = True


class GrabPuckIT(IntegrationContext):
    def __init__(self):
        super().__init__(local_flag=False)

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

            # TODO Fix le dernier mouvement pour arriver un peu avant la puck
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
            return self._vision_service.find_puck_position(color)
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


if __name__ == "__main__":
    grab_puck_it = GrabPuckIT()

    print("Sending start command")
    grab_puck_it.send_command_to_robot(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)
    grab_puck_it.wait_for_robot_confirmation(Topic.START_CYCLE)

    print("Rotating robot")
    grab_puck_it._rotation_service.rotate(CardinalOrientation.SOUTH.value)

    print("Finding robot position")
    first_stage_robot_pose = grab_puck_it.find_robot_pose()
    # TODO Find gripper position for real

    print("Finding puck position")
    puck_position = grab_puck_it.find_puck_position(PUCK_COLOR_TO_USE)

    print("Finding movements to puck")
    movements_to_puck = grab_puck_it.find_movements_to_goal(
        first_stage_robot_pose, puck_position
    )

    # TODO Rotate robot

    print("Sending path to robot")
    grab_puck_it.send_command_to_robot(Topic.MOVEMENTS, movements_to_puck)

    print("Waiting for robot to move")
    grab_puck_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

    print("Send command to grab puck to robot")
    grab_puck_it.send_command_to_robot(Topic.GRAB_PUCK, PUCK_COLOR_TO_USE)

    print("Waiting for robot to grab puck")
    grab_puck_it.wait_for_robot_confirmation(Topic.GRAB_PUCK)

    print("Finding robot position")
    grab_puck_it.find_robot_pose()
    second_stage_robot_pose = grab_puck_it.find_robot_pose()
    # TODO Find gripper position for real

    print("Finding movements to starting zone center")
    movements_to_starting_zone = grab_puck_it.find_movements_to_starting_zone(
        second_stage_robot_pose
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
