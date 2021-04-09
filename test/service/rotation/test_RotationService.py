from unittest import TestCase
from unittest.mock import MagicMock

from domain.Orientation import Orientation
from domain.RobotPose import RobotPose
from domain.communication.Message import Message
from domain.game.Topic import Topic
from service.rotation.RotationService import RotationService


class TestRotationService(TestCase):
    AN_IMAGE = MagicMock()
    A_POSITION = MagicMock()
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

    def test_givenRobotNotCorrectlyOriented_whenRotate_thenSendAdjustedOrientation(
        self,
    ):
        self._setup_communication_service(1)
        self._setup_vision_service(self.ANOTHER_ORIENTATION)
        expected_orientation = self.ANOTHER_ORIENTATION - self.AN_ORIENTATION

        self._rotation_service.rotate(self.AN_ORIENTATION)

        self._communication_service.send_object.assert_called_with(
            Message(Topic.ROTATION, expected_orientation)
        )

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
