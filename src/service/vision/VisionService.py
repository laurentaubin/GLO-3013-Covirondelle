from domain import StartingZone
from domain.GameTable import GameTable
from domain.Position import Position
from domain.camera.IWorldCamera import IWorldCamera
from domain.game.GameState import GameState
from domain.pathfinding.Maze import Maze
from domain.vision.IRobotDetector import IRobotDetector
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from domain.vision.ITableDetector import ITableDetector


class VisionService:
    def __init__(
        self,
        starting_zone_corner_detector: IStartingZoneDetector,
        table_detector: ITableDetector,
        world_camera: IWorldCamera,
        robot_detector: IRobotDetector,
    ) -> None:
        self._starting_zone_corner_detector = starting_zone_corner_detector
        self._table_detector = table_detector
        self._world_camera = world_camera
        self._world_image = world_camera.take_world_image()
        self._robot_detector = robot_detector

    def find_robot_position(self, image) -> Position:
        pass

    def create_game_table(self) -> GameTable:
        table_image = self._table_detector.crop_table(self._world_image)

        starting_zone = self._find_starting_zone(table_image)
        maze = self._create_maze(table_image)
        # TODO add pucks to game table

        return GameTable(starting_zone, maze)

    def get_vision_state(self):
        world_image = self._world_camera.take_world_image()
        robot_pose = self._robot_detector.detect(world_image)
        return world_image, robot_pose

    def _find_starting_zone(self, table_image) -> StartingZone:
        return self._starting_zone_corner_detector.detect(table_image)

    def _create_maze(self, image) -> Maze:
        image_width, image_height, _ = image.shape
        maze = Maze(width=image_width, height=image_height)

        # TODO add obstacles to maze

        return maze
