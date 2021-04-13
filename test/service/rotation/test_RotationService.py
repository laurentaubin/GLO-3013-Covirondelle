from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.communication.Message import Message
from domain.game.Topic import Topic
from service.rotation.RotationService import RotationService


class TestRotationService(TestCase):
    AN_IMAGE = MagicMock()
    A_POSITION = Position(100, 100)
    ANOTHER_POSITION = Position(200, 200)
    A_ROBOT_POSE = MagicMock()
    AN_ORIENTATION = Orientation(20)
    ANOTHER_ORIENTATION = Orientation(254)

    def setUp(self) -> None:
        self._communication_service = MagicMock()
        self._vision_service = MagicMock()
        self._rotation_service = RotationService(
            self._vision_service, self._communication_service
        )

    def test_whenRotate_thenGetVisionState(self):
        self._setup_vision_service()

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._vision_service.get_vision_state.assert_called()

    def test_givenRobotNotCorrectlyOriented_whenRotate_thenSendRotationToRobot(self):
        self._setup_communication_service(1)
        self._setup_vision_service(self.ANOTHER_ORIENTATION)

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.send_object.assert_called()

    def test_givenRobotNotCorrectlyOriented_whenRotate_thenReceiveRotationCompletedConfirmationFromRobot(
        self,
    ):
        self._communication_service(1)
        self._setup_vision_service(self.ANOTHER_ORIENTATION)

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.receive_object.assert_called()

    def test_givenRobotCorrectlyOriented_whenRotate_thenDontSendRotationToRobot(self):
        self._setup_vision_service()

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.send_object.assert_not_called()

    def test_givenRobotCorrectlyOriented_whenRotate_thenDontReceiveAnythingFromRobot(
        self,
    ):
        self._setup_vision_service()

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.receive_object.assert_not_called()

    def test_givenRobotAlreadyInCorrectOrientation_whenRotate_thenShouldGetVisionStateOneTime(
        self,
    ):
        self._setup_communication_service(1)
        self._setup_vision_service()

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self.assertEqual(1, self._vision_service.get_vision_state.call_count)

    def test_givenRobotNotInitiallyInCorrectOrientation_whenRotate_thenGetVisionStateShouldBeCalledTwoTimesForValidation(
        self,
    ):
        self._setup_communication_service(2)
        self._setup_vision_service(self.ANOTHER_ORIENTATION)

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self.assertEqual(2, self._vision_service.get_vision_state.call_count)

    def test_givenRobotNotCorrectlyOrientedAndRobotWithOrientationLargerThan180Degree_whenRotate_thenSendNegativeAdjustedOrientation(
        self,
    ):
        self._setup_communication_service(1)
        self._setup_vision_service(self.ANOTHER_ORIENTATION)
        expected_orientation = Orientation(-126)

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.send_object.assert_called_with(
            Message(Topic.ROTATION, expected_orientation)
        )

    @patch("infra.utils.GeometryUtils.GeometryUtils.calculate_angle_between_positions")
    def test_whenFindOrientationToPuck_thenFindAngleBetweenRobotAndPuck(
        self, geometryUtils_mock
    ):
        self.A_ROBOT_POSE.get_position.return_value = self.A_POSITION

        self._rotation_service.find_orientation_to_puck(
            self.ANOTHER_POSITION, self.A_ROBOT_POSE
        )

        geometryUtils_mock.assert_called_with(self.A_POSITION, self.ANOTHER_POSITION)

    @patch("infra.utils.GeometryUtils.GeometryUtils.calculate_angle_between_positions")
    def test_givenCalculatedAngleOf90AndRobotOrientationOfZero_whenFindAngleBetweenRobotAndPuck_thenReturn90(
        self, geometryUtils_mock
    ):
        geometryUtils_mock.return_value = Orientation(90)
        self.A_ROBOT_POSE.get_orientation_in_degree.return_value = Orientation(0)
        expected_orientation = Orientation(90)

        actual_orientation = self._rotation_service.find_orientation_to_puck(
            self.A_POSITION, self.A_ROBOT_POSE
        )

        self.assertEqual(expected_orientation, actual_orientation)

    @patch("infra.utils.GeometryUtils.GeometryUtils.calculate_angle_between_positions")
    def test_givenCalculatedAngleOf48AndRobotOrientationOf90_whenFindAngleBetweenRobotAndPuck_thenReturnNegative42(
        self, geometryUtils_mock
    ):
        geometryUtils_mock.return_value = Orientation(48)
        self.A_ROBOT_POSE.get_orientation_in_degree.return_value = Orientation(90)
        expected_orientation = Orientation(-42)

        actual_orientation = self._rotation_service.find_orientation_to_puck(
            self.A_POSITION, self.A_ROBOT_POSE
        )

        self.assertEqual(expected_orientation, actual_orientation)

    def _setup_communication_service(self, number_of_rotation_message_send: int):
        side_effect = []
        for i in range(number_of_rotation_message_send):
            side_effect.append(Message(Topic.ROTATION_COMPLETED, None))
        self._communication_service.receive_object.side_effect = side_effect

    def _setup_vision_service(self, first_robot_orientation=AN_ORIENTATION):
        first_robot_pose = RobotPose(self.A_POSITION, first_robot_orientation)
        a_robot_pose = RobotPose(self.A_POSITION, self.AN_ORIENTATION)
        self._vision_service.get_vision_state.side_effect = [
            (self.AN_IMAGE, first_robot_pose),
            (self.AN_IMAGE, a_robot_pose),
        ]
