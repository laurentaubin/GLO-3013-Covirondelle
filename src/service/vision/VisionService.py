from domain import StartingZone
from domain.GameTable import GameTable
from domain.Position import Position
from domain.camera.ICalibrator import ICalibrator
from domain.camera.IWorldCamera import IWorldCamera
from domain.pathfinding.Maze import Maze
from domain.pathfinding.MazeFactory import MazeFactory
from domain.vision.IObstacleDetector import IObstacleDetector
from domain.vision.IRobotDetector import IRobotDetector
from domain.vision.IStartingZoneDetector import IStartingZoneDetector
from domain.vision.ITableDetector import ITableDetector


class VisionService:
    def __init__(
        self,
        starting_zone_corner_detector: IStartingZoneDetector,
        obstacle_detector: IObstacleDetector,
        calibrator: ICalibrator,
        table_detector: ITableDetector,
        world_camera: IWorldCamera,
        maze_factory: MazeFactory,
        robot_detector: IRobotDetector,
    ) -> None:
        self._starting_zone_corner_detector = starting_zone_corner_detector
        self._obstacle_detector = obstacle_detector
        self._calibrator = calibrator
        self._table_detector = table_detector
        self._world_camera = world_camera
        self._world_image = world_camera.take_world_image()
        self._maze_factory = maze_factory
        self._robot_detector = robot_detector

    def find_robot_position(self, image) -> Position:
        return self._robot_detector.detect(image)

    def create_game_table(self) -> GameTable:
        table_image = self._get_calibrated_table_image(self._world_image)

        starting_zone = self._find_starting_zone(table_image)
        maze = self._create_maze(table_image)

        return GameTable(starting_zone, maze)

    def get_vision_state(self):
        world_image = self._world_camera.take_world_image()
        robot_pose = self.find_robot_position(world_image)
        return world_image, robot_pose

    def _find_starting_zone(self, table_image) -> StartingZone:
        return self._starting_zone_corner_detector.detect(table_image)

    def _create_maze(self, image) -> Maze:
        obstacles_on_table = self._obstacle_detector.detect(image)
        return self._maze_factory.create_from_shape_and_obstacles(
            image.shape, obstacles_on_table
        )

    def _get_calibrated_table_image(self, image):
        return self._calibrator.calibrate(image)
        # return self._table_detector.crop_table(undistorted_image)
