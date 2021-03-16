from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()
    UNDISTORTED_TABLE_IMAGE = MagicMock()
    AN_IMAGE_SHAPE = [120, 200, 3]
    A_ROBOT_POSE = MagicMock()

    game_state = MagicMock()
    starting_zone_detector = MagicMock()
    table_detector = MagicMock()
    world_camera = MagicMock()
    robot_detector = MagicMock()

    def setUp(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.vision_service = VisionService(
            self.starting_zone_detector,
            self.table_detector,
            self.world_camera,
            self.robot_detector,
        )

        self.table_detector.crop_table.return_value = self.AN_IMAGE
        self.AN_IMAGE.shape = self.AN_IMAGE_SHAPE

    def test_whenCreateGameTable_thenStartingZoneDetectorUseUndistortedTableImage(self):
        self.UNDISTORTED_TABLE_IMAGE.shape = self.AN_IMAGE_SHAPE

        self.vision_service.create_game_table()

        self.starting_zone_detector.detect.assert_called_with(self.AN_IMAGE)

    def test_whenCreateGameTable_thenGameTableContainsStartingZoneDetected(self):
        self.starting_zone_detector.detect.return_value = self.A_STARTING_ZONE

        actual_starting_zone = (
            self.vision_service.create_game_table().get_starting_zone()
        )

        self.assertEqual(self.A_STARTING_ZONE, actual_starting_zone)

    def test_givenWorldCameraTakesPictureOfTable_createGameTable_thenMazeHasRightDimensions(
        self,
    ):
        actual_maze = self.vision_service.create_game_table().get_maze()
        maze_width, maze_height = actual_maze.get_shape()

        self.assertEqual(maze_width, self.AN_IMAGE_SHAPE[0])
        self.assertEqual(maze_height, self.AN_IMAGE_SHAPE[1])

    def test_whenGetVisionState_thenTableImageIsTaken(self):
        self.vision_service.get_vision_state()

        self.world_camera.take_world_image.assert_called()

    def test_whenGetVisionState_thenRobotIsDetected(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE

        self.vision_service.get_vision_state()

        self.robot_detector.detect.assert_called_with(self.AN_IMAGE)

    def test_whenGetVisionState_thenTableImageAndRobotPoseAreReturned(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.robot_detector.detect.return_value = self.A_ROBOT_POSE

        actual_table_image, actual_robot_pose = self.vision_service.get_vision_state()

        self.assertEqual(actual_table_image, self.AN_IMAGE)
        self.assertEqual(actual_robot_pose, self.A_ROBOT_POSE)
