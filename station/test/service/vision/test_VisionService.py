from unittest import TestCase
from unittest.mock import MagicMock, call

from domain.Color import Color
from domain.Position import Position
from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_STARTING_ZONE = MagicMock()
    AN_IMAGE = MagicMock()
    UNDISTORTED_TABLE_IMAGE = MagicMock()
    PUCK_ZONE_CENTER = Position(100, 200)
    AN_IMAGE_SHAPE = [120, 200, 3]
    A_POSITION_LIST = [Position(100, 100), Position(200, 200)]
    A_MAZE = MagicMock()
    A_ROBOT_POSE = MagicMock()
    A_POSITION = MagicMock()
    A_COLOR = Color.BLUE
    SOME_PUCKS = MagicMock()

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
            self.PUCK_ZONE_CENTER,
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

    def test_whenCreateGameTable_thenWorldImageIsTaken(self):
        self.vision_service.create_game_table()

        self.world_camera.take_world_image.assert_called()

    def test_whenCreateGameTable_thenStartingZoneDetectorUseWorldImage(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE

        self.vision_service.create_game_table()

        self.starting_zone_detector.detect.assert_called_with(self.AN_IMAGE)

    def test_whenCreateGameTable_thenGameTableContainsStartingZoneDetected(self):
        self.starting_zone_detector.detect.return_value = self.A_STARTING_ZONE

        actual_starting_zone = (
            self.vision_service.create_game_table().get_starting_zone()
        )

        self.assertEqual(self.A_STARTING_ZONE, actual_starting_zone)

    def test_whenCreateGameTable_thenObstaclesAreDetectedUsingUndistortedImage(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.UNDISTORTED_TABLE_IMAGE.shape = self.AN_IMAGE_SHAPE

        self.vision_service.create_game_table()

        self.obstacle_detector.detect.assert_called_with(self.AN_IMAGE)

    def test_whenCreateGameTable_thenGameTableHasRightPuckZonePosition(self):
        game_table = self.vision_service.create_game_table()

        self.assertEqual(self.PUCK_ZONE_CENTER, game_table.get_puck_zone_center())

    def test_givenWorldCameraTakesPictureOfTable_createGameTable_thenMazeIsCreatedWithRightDimensionsAndObstacles(
        self,
    ):
        self.image_calibrator.calibrate.return_value = self.AN_IMAGE

        self.vision_service.create_game_table()

        self.maze_factory.create_from_shape_and_obstacles_and_pucks_as_obstacles.assert_called()

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

    def test_whenCreateGameTable_thenAllPucksAreDetected(self):
        self.world_camera.take_world_image.return_value = self.AN_IMAGE
        self.image_calibrator.calibrate.return_value = self.AN_IMAGE
        expected_calls = [
            call(self.AN_IMAGE, color) for color in Color if color != Color.NONE
        ]

        self.vision_service.create_game_table()

        self.puck_detector.detect.assert_has_calls(expected_calls)

    def test_givenPucksDetected_whenCreateGameTable_thenGameTableHasPucks(self):
        self.puck_detector.detect.return_value = self.A_POSITION
        puck_colors = len(Color) - 1

        actual_game_table = self.vision_service.create_game_table()

        self.assertEqual(len(actual_game_table.get_pucks()), puck_colors)
