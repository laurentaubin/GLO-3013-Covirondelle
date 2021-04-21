from domain.CardinalOrientation import CardinalOrientation
from domain.Orientation import Orientation
from domain.Position import Position
from domain.Puck import Puck
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


class TransportPuckHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        path_service: PathService,
        rotation_service: RotationService,
        _movement_factory: MovementFactory,
    ):
        self._communication_service = communication_service
        self._path_service = path_service
        self._rotation_service = rotation_service
        self._movement_factory = _movement_factory

    def execute(self):
        GameState.get_instance().set_current_stage(Stage.TRANSPORT_PUCK)

        puck_colors = GameState.get_instance().get_puck_colors()

        pucks_to_grab = [
            GameState.get_instance().get_game_table().get_puck(color)
            for color in puck_colors
        ]

        for puck in pucks_to_grab:
            print(puck.get_color(), puck.get_position())

        self._send_command_to_robot(Topic.START_STAGE, Stage.TRANSPORT_PUCK)
        self._wait_for_robot_confirmation(Topic.START_STAGE)

        for starting_zone_corner_index, puck in enumerate(pucks_to_grab):
            GameState.get_instance().set_current_puck(puck.get_color())

            self._go_to_puck_zone()
            self._go_to_puck_zone()
            self._grab_puck(puck)
            self._go_back_to_puck_zone()
            self._go_to_starting_zone_center()
            self._go_to_starting_zone_center()
            self._rotate_robot_towards_corner(starting_zone_corner_index)
            self._go_forward_a_bit()
            self._drop_puck_on_corner()
            self._add_puck_as_obstacle(starting_zone_corner_index, puck)
            self._go_back_a_bit()
            self._go_to_starting_zone_center()

        self._send_command_to_robot(Topic.STAGE_COMPLETED, None)
        self._wait_for_robot_confirmation(Topic.STAGE_COMPLETED)

    def _go_to_starting_zone_center(self):
        # TODO Maybe get this out of here to now look clanky at the beginning of the stage
        self._rotation_service.rotate(CardinalOrientation.EAST.value)
        robot_pose = self._find_robot_pose()
        movements_to_starting_zone = self._find_movements_to_starting_zone(robot_pose)
        self._move_robot(movements_to_starting_zone)

    def _go_to_puck_zone(self):
        self._rotation_service.rotate(CardinalOrientation.WEST.value)
        robot_pose = self._find_robot_pose()
        movements_to_puck_zone = self._find_movements_to_puck_zone(robot_pose)
        self._move_robot(movements_to_puck_zone)

    def _grab_puck(self, puck: Puck):
        puck_position = puck.get_position()
        if self._puck_is_close_to_center_middle(puck):
            self._move_robot([Movement(Direction.BACKWARDS, Distance(0.2))])

        robot_pose = self._find_robot_pose()
        orientation_to_puck = self._find_orientation_to_puck(puck_position, robot_pose)
        self._rotation_service.rotate(orientation_to_puck)

        # movements_to_puck = self._create_straight_movement(
        #     Direction.FORWARD, puck_position, robot_pose
        # )

        movements_to_puck = [
            Movement(
                Direction.FORWARD, Distance(0.1, unit_of_measure=UnitOfMeasure.METER)
            )
        ]
        print(
            movements_to_puck[0].get_direction(),
            movements_to_puck[0].get_distance().get_distance(),
        )
        self._move_robot(movements_to_puck)
        self._send_command_to_robot(
            Topic.GRAB_PUCK, puck.get_color().get_resistance_digit()
        )
        self._wait_for_robot_confirmation(Topic.GRAB_PUCK)

    def _go_back_to_puck_zone(self):
        robot_pose = self._find_robot_pose()
        movements_back_to_puck_zone = [
            Movement(
                Direction.BACKWARDS, Distance(0.15, unit_of_measure=UnitOfMeasure.METER)
            )
        ]
        self._move_robot(movements_back_to_puck_zone)

    def _drop_puck_on_corner(self):
        self._send_command_to_robot(Topic.DROP_PUCK, None)
        self._wait_for_robot_confirmation(Topic.DROP_PUCK)

    def _rotate_robot_towards_corner(self, starting_zone_corner_index):
        starting_zone_corner_orientation = (
            GameState.get_instance()
            .get_starting_zone_corners()[starting_zone_corner_index]
            .value
        )
        self._rotate_robot(starting_zone_corner_orientation)

    def _move_robot(self, movements):
        self._send_command_to_robot(Topic.MOVEMENTS, movements)
        self._wait_for_robot_confirmation(Topic.MOVEMENTS)

    def _create_straight_movement(
        self,
        direction: Direction,
        goal_position: Position,
        robot_pose: RobotPose,
    ):
        # TODO Fix it so we calculate diagonal path to avoid it looking dumb in the UI
        path = self._path_service.find_path(robot_pose.get_position(), goal_position)
        GameState.get_instance().set_current_planned_trajectory(path)

        position_to_use = (
            robot_pose.get_gripper_position()
            if direction is Direction.FORWARD
            else robot_pose.get_position()
        )

        return [
            self._movement_factory.create_movement_to_get_to_point_with_direction(
                position_to_use,
                goal_position,
                direction,
            )
        ]

    def _send_command_to_robot(self, command: Topic, payload: object):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _find_robot_pose(self):
        return GameState.get_instance().get_robot_pose()

    def _wait_for_robot_confirmation(self, topic: Topic):
        robot_response = self._communication_service.receive_object()
        if robot_response.get_topic() == topic:
            return
        else:
            print("Wrong command whoops !")

    def _rotate_robot(self, wanted_orientation: Orientation):
        self._rotation_service.rotate(wanted_orientation)

    def _find_movements_to_starting_zone(self, robot_pose):
        path = self._path_service.find_path_to_starting_zone_center(
            robot_pose.get_position()
        )
        GameState.get_instance().set_current_planned_trajectory(path)

        return self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def _find_movements_to_puck_zone(self, robot_pose: RobotPose):
        path = self._path_service.find_path_to_puck_zone_center(
            robot_pose.get_position()
        )
        GameState.get_instance().set_current_planned_trajectory(path)

        return self._movement_factory.create_movements(
            path, robot_pose.get_orientation_in_degree()
        )

    def _find_orientation_to_puck(self, puck_position, robot_pose):
        return self._rotation_service.find_orientation_to_puck(
            puck_position, robot_pose
        )

    def _go_forward_a_bit(self):
        movements = [
            Movement(
                Direction.FORWARD, Distance(0.25, unit_of_measure=UnitOfMeasure.METER)
            )
        ]
        self._move_robot(movements)

    def _go_back_a_bit(self):
        movements = [
            Movement(
                Direction.BACKWARDS, Distance(0.2, unit_of_measure=UnitOfMeasure.METER)
            )
        ]
        self._move_robot(movements)

    def _puck_is_close_to_center_middle(self, puck: Puck):
        return puck.get_position().get_x_coordinate() < 920

    def _add_puck_as_obstacle(self, starting_zone_corner_index: int, puck: Puck):
        maze = GameState.get_instance().get_game_table().get_maze()
        starting_zone = GameState.get_instance().get_game_table().get_starting_zone()
        current_corner = GameState.get_instance().get_starting_zone_corners()[
            starting_zone_corner_index
        ]
        corner_position = starting_zone.find_corner_position_from_letter(current_corner)
        maze.add_puck_as_obstacle(corner_position)
        maze.remove_puck_as_obstacle(puck.get_position())
