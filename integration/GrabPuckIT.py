from domain.Position import Position
from domain.StartingZoneCorner import StartingZoneCorner
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.Color import Color
from domain.game.Topic import Topic

from domain.movement.MovementFactory import MovementFactory
from integration.IntegrationContext import IntegrationContext


PUCK_COLOR_TO_USE = Color.YELLOW
STARTING_ZONE_CORNER_TO_USE = StartingZoneCorner.B


DETECT_PUCK_FOR_REAL = True
DETECT_ROBOT_FOR_REAL = True
DETECT_STARTING_ZONE_FOR_REAL = True
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

    def find_movements_to_goal(self, robot_position, goal_position):
        if FIND_MOVEMENTS_FOR_REAL:
            path = self._path_service.find_path(robot_position, goal_position)

            # TODO Fix le dernier mouvement pour arriver un peu avant la puck
            return MovementFactory().create_movements(path)
        else:
            # TODO return hardcoded movements
            pass

    def send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def find_robot_position(self):
        if DETECT_ROBOT_FOR_REAL:
            _, robot_pose = self._vision_service.get_vision_state()
            return robot_pose.get_position()
        else:
            # TODO return hardcoded position
            pass

    def find_puck_position(self, color: Color):
        if DETECT_PUCK_FOR_REAL:
            return self._vision_service.find_puck_position(color)
        else:
            # TODO return hardcoded puck
            pass

    def find_starting_zone_corner_position(self):
        if DETECT_STARTING_ZONE_FOR_REAL:
            starting_zone = self._vision_service.create_game_table().get_starting_zone()
            return starting_zone.find_corner_position_from_letter(
                STARTING_ZONE_CORNER_TO_USE
            )
        else:
            # TODO return hardcoded corner position
            pass

    def wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            return
        else:
            print("Wrong command whoops !")


if __name__ == "__main__":
    grab_puck_it = GrabPuckIT()

    print("Sending start command")
    grab_puck_it.send_command_to_robot(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)
    grab_puck_it.wait_for_robot_confirmation(Topic.START_CYCLE)

    print("Finding robot position")
    first_stage_robot_position = grab_puck_it.find_robot_position()
    # TODO Find gripper position for real
    first_stage_gripper_position = first_stage_robot_position + Position(175, 0)

    print("Finding puck position")
    puck_position = grab_puck_it.find_puck_position(PUCK_COLOR_TO_USE)

    print("Finding movements to puck")
    movements_to_puck = grab_puck_it.find_movements_to_goal(
        first_stage_gripper_position, puck_position
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
    grab_puck_it.find_robot_position()
    second_stage_robot_position = grab_puck_it.find_robot_position()
    # TODO Find gripper position for real
    second_stage_gripper_position = second_stage_robot_position + Position(140, 0)

    print("Finding starting zone corner position")
    starting_zone_corner_position = grab_puck_it.find_starting_zone_corner_position()

    print("Finding movements to starting zone")
    movements_to_starting_zone = grab_puck_it.find_movements_to_goal(
        second_stage_gripper_position, starting_zone_corner_position
    )

    print("Sending movements to robot")
    grab_puck_it.send_command_to_robot(Topic.MOVEMENTS, movements_to_starting_zone)

    print("Waiting for robot to move")
    grab_puck_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

    print("Sending command to drop puck")
    grab_puck_it.send_command_to_robot(Topic.DROP_PUCK, None)

    print("Waiting for robot to drop puck")
    grab_puck_it.wait_for_robot_confirmation(Topic.DROP_PUCK)

    print("Wrapping up stage")
    grab_puck_it.send_command_to_robot(Topic.STAGE_COMPLETED, None)
    grab_puck_it.wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

    print("Stage complete")
