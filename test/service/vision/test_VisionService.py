from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()
    UNDISTORTED_IMAGE = MagicMock()

    UNDISTORTED_TABLE_IMAGE = MagicMock()
    AN_IMAGE_SHAPE = [120, 200, 3]

    def setUp(self):
        self.starting_zone_detector = MagicMock()
        self.image_calibrator = MagicMock()
        self.table_detector = MagicMock()
        self.world_camera = MagicMock()
        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.vision_service = VisionService(
            self.starting_zone_detector,
            self.image_calibrator,
            self.table_detector,
            self.world_camera,
        )

        self.table_detector.crop_table.return_value = self.AN_IMAGE
        self.AN_IMAGE.shape = self.AN_IMAGE_SHAPE

    def test_whenCreateGameTable_thenImageIsUndistorted(self):
        self.vision_service.create_game_table()

        self.image_calibrator.calibrate.assert_called_with(self.AN_IMAGE)

    def test_whenCreateGameTable_thenTableIsDetectedFromUndistortedImage(self):
        self.image_calibrator.calibrate.return_value = self.UNDISTORTED_IMAGE

        self.vision_service.create_game_table()

        self.table_detector.crop_table.assert_called_with(self.UNDISTORTED_IMAGE)

    def test_whenCreateGameTable_thenStartingZoneDetectorUseUndistortedTableImage(self):
        self.table_detector.crop_table.return_value = self.UNDISTORTED_TABLE_IMAGE
        self.UNDISTORTED_TABLE_IMAGE.shape = self.AN_IMAGE_SHAPE

        self.vision_service.create_game_table()

        self.starting_zone_detector.detect.assert_called_with(
            self.UNDISTORTED_TABLE_IMAGE
        )

    def test_whenCreateGameTable_thenGameTableContainsStartingZoneDetected(self):
        self.starting_zone_detector.detect.return_value = self.A_STARTING_ZONE

        actual_starting_zone = (
            self.vision_service.create_game_table().get_starting_zone()
        )

        self.assertEqual(self.A_STARTING_ZONE, actual_starting_zone)

    def test_givenAnImage_whenFindRobotPosition_thenImageIsUndistorted(self):
        self.vision_service.find_robot_position(self.AN_IMAGE)

        self.image_calibrator.calibrate.assert_called_with(self.AN_IMAGE)

    def test_givenWorldCameraTakesPictureOfTable_createGameTable_thenMazeHasRightDimensions(
        self,
    ):

        actual_maze = self.vision_service.create_game_table().get_maze()
        maze_width, maze_height = actual_maze.get_shape()

        self.assertEqual(maze_width, self.AN_IMAGE_SHAPE[0])
        self.assertEqual(maze_height, self.AN_IMAGE_SHAPE[1])
