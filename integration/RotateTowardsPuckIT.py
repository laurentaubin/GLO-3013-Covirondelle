from IntegrationContext import IntegrationContext
from domain.CardinalOrientation import CardinalOrientation
from domain.Color import Color
from domain.Orientation import Orientation
from domain.RobotPose import RobotPose
from domain.UnitOfMeasure import UnitOfMeasure
from domain.communication.Message import Message
from domain.game.Topic import Topic
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementFactory import MovementFactory

PUCK_COLOR_TO_USE = Color.YELLOW

DETECT_PUCK_FOR_REAL = True
DETECT_ROBOT_FOR_REAL = True
FIND_MOVEMENTS_FOR_REAL = True


class RotateTowardsPuckIT(IntegrationContext):
    def __init__(self):
        super().__init__(False)

    def find_puck_position(self, color: Color):
        if DETECT_PUCK_FOR_REAL:
            return self._path_service._game_table.get_puck(color).get_position()
        else:
            # TODO return hardcoded puck
            pass

    def find_robot_pose(self):
        if DETECT_ROBOT_FOR_REAL:
            _, robot_pose = self._vision_service.get_vision_state()
            return robot_pose
        else:
            # TODO return hardcoded position
            pass

    def find_orientation_to_puck(self, puck_position, robot_pose):
        return self._rotation_service.find_orientation_to_puck(
            puck_position, robot_pose
        )

    def send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            return
        else:
            print("Wrong command whoops !")

    def run(self):
        print("Finding puck position")
        current_puck_position = rotate_it.find_puck_position(PUCK_COLOR_TO_USE)

        input("Put robot in the middle of the puck zone")

        print("Finding robot position")
        puck_zone_robot_pose = rotate_it.find_robot_pose()

        print("Finding angle between puck and robot")
        orientation_to_puck = rotate_it.find_orientation_to_puck(
            current_puck_position, puck_zone_robot_pose
        )

        print("Rotating to face puck")
        rotate_it._rotation_service.rotate(orientation_to_puck)

        print("Calculating movement needed to get to puck")
        movements_to_puck = [
            MovementFactory().create_movement_to_get_to_point_with_direction(
                puck_zone_robot_pose.get_gripper_position(),
                current_puck_position,
                Direction.FORWARD,
            )
        ]

        print("Sending movements to robot")
        rotate_it.send_command_to_robot(Topic.MOVEMENTS, movements_to_puck)

        print("Waiting for robot to move")
        rotate_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

        print("Send command to grab puck to robot")
        rotate_it.send_command_to_robot(
            Topic.GRAB_PUCK, PUCK_COLOR_TO_USE.get_resistance_digit()
        )

        print("Waiting for robot to grab puck")
        rotate_it.wait_for_robot_confirmation(Topic.GRAB_PUCK)

        print("Finding robot position")
        robot_with_puck_pose = rotate_it.find_robot_pose()

        print("Calculating movement needed to go back to puck zone center")

        movements_back_to_puck_zone = [
            MovementFactory().create_movement_to_get_to_point_with_direction(
                robot_with_puck_pose.get_gripper_position(),
                current_puck_position,
                Direction.BACKWARDS,
            )
        ]

        print("Sending movements to robot")
        rotate_it.send_command_to_robot(Topic.MOVEMENTS, movements_back_to_puck_zone)

        print("Waiting for robot to move")
        rotate_it.wait_for_robot_confirmation(Topic.MOVEMENTS)

        print("Rotating robot straight")
        rotate_it._rotation_service.rotate(CardinalOrientation.EAST.value)


if __name__ == "__main__":
    rotate_it = RotateTowardsPuckIT()
    rotate_it.run()
