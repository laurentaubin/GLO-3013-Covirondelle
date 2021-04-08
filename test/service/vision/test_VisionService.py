from unittest import TestCase
from unittest.mock import MagicMock

from domain.Color import Color
from domain.Position import Position
from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()
    UNDISTORTED_TABLE_IMAGE = MagicMock()
    AN_IMAGE_SHAPE = [120, 200, 3]
    A_POSITION_LIST = [Position(100, 100), Position(200, 200)]
    A_MAZE = MagicMock()
    A_ROBOT_POSE = MagicMock()
    A_POSITION = MagicMock()
    A_COLOR = Color.BLUE

    def setUp(self):
        self.setUpMocks()

        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.vision_service = VisionService(
            self.starting_zone_detector,
            self.obstacle_detector,
            self.image_calibrator,
            self.table_detector,
            self.world_camera,
            self.maze_factory,
            self.robot_detector,
            self.puck_detector,
        )

        self.table_detector.crop_table.return_value = self.AN_IMAGE
        self.obstacle_detector.detect.return_value = self.A_POSITION_LIST
        self.AN_IMAGE.shape = self.AN_IMAGE_SHAPE

    def setUpMocks(self):
        self.starting_zone_detector = MagicMock()
        self.obstacle_detector = MagicMock()
        self.image_calibrator = MagicMock()
        self.table_detector = MagicMock()
        self.world_camera = MagicMock()
        self.maze_factory = MagicMock()
        self.robot_detector = MagicMock()
        self.puck_detector = MagicMock()

    def test_whenCreateGameTable_thenImageIsUndistorted(self):
        self.vision_service.create_game_table()

        self.image_calibrator.calibrate.assert_called_with(self.AN_IMAGE)

    def test_whenCreateGameTable_thenStartingZoneDetectorUseUndistortedTableImage(self):
        self.image_calibrator.calibrate.return_value = self.UNDISTORTED_TABLE_IMAGE

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

    def test_whenCreateGameTable_thenObstaclesAreDetectedUsingUndistortedImage(self):
        self.image_calibrator.calibrate.return_value = self.UNDISTORTED_TABLE_IMAGE
        self.UNDISTORTED_TABLE_IMAGE.shape = self.AN_IMAGE_SHAPE

        self.vision_service.create_game_table()

        self.obstacle_detector.detect.assert_called_with(self.UNDISTORTED_TABLE_IMAGE)

    def test_givenWorldCameraTakesPictureOfTable_createGameTable_thenMazeIsCreatedWithRightDimensionsAndObstacles(
        self,
    ):
        self.image_calibrator.calibrate.return_value = self.AN_IMAGE

        self.vision_service.create_game_table()

        self.maze_factory.create_from_shape_and_obstacles.assert_called_with(
            self.AN_IMAGE_SHAPE, self.A_POSITION_LIST
        )

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

    def test_givenColorAndCalibratedTableImage_whenFindPuck_thenUsePuckDetectorToDetectRightColor(
        self,
    ):
        self.image_calibrator.calibrate.return_value = self.AN_IMAGE
        a_color = Color.YELLOW

        self.vision_service.find_puck_position(a_color)

        self.puck_detector.detect.assert_called_with(self.AN_IMAGE, a_color)

    def test_givenPuckDetectedByDetector_whenFindPuck_thenReturnPuckPosition(self):
        self.puck_detector.detect.return_value = self.A_POSITION

        actual_position = self.vision_service.find_puck_position(self.A_COLOR)

        self.assertEqual(self.A_POSITION, actual_position)
