from unittest import TestCase
from unittest.mock import MagicMock

from domain.communication.message import Message
from domain.gripper.GripperStatus import GripperStatus
from service.communication.CommunicationService import CommunicationService

STATUS_HAS_PUCK = GripperStatus.HAS_PUCK


class TestCommunicationService(TestCase):
    A_MESSAGE = Message("a task", False)

    def setUp(self):
        self.pub_sub_connector = MagicMock()
        self.game_cycle_connector = MagicMock()
        self.robot_information = MagicMock()
        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.pub_sub_connector, self.robot_information
        )

    def test_whenReceiveMessage_thenConnectorReceivesMessage(self):
        self.communication_service.receive_game_cycle_message()

        self.assertTrue(self.game_cycle_connector.receive_message.called)

    def test_whenSendMessage_thenConnectorSendsMessage(self):
        self.communication_service.send_game_cycle_message(self.A_MESSAGE)

        self.assertTrue(
            self.game_cycle_connector.send_message.called_with(self.A_MESSAGE)
        )

    def test_whenReceiveObject_thenConnectorIsUsedToReceiveObject(self):
        an_object = MagicMock()
        self.game_cycle_connector.receive_object.return_value = an_object

        actual_object = self.communication_service.receive_object()

        self.assertEqual(an_object, actual_object)

    def test_givenStatusReturnByRobotInformation_whenSendGripperStatus_thenPublishStatus(
        self,
    ):
        self.robot_information.get_gripper_status.return_value = STATUS_HAS_PUCK

        self.communication_service.send_gripper_status()

        self.pub_sub_connector.publish_gripper_status.assert_called_with(
            STATUS_HAS_PUCK
        )
