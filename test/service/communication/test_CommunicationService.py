from unittest import TestCase
from unittest.mock import MagicMock

from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = "a message"
    SOCKET_ADDRESS = "a socket address"
    A_PATH = MagicMock()

    def setUp(self):
        self.game_cycle_connector = MagicMock()
        self.robot_update_connector = MagicMock()
        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.robot_update_connector
        )

    def test_givenStatusPublishedByRobot_whenReceiveRobotStatus_thenStatusConnectorReceivesMessage(
        self,
    ):
        self.communication_service.receive_robot_status()

        self.robot_update_connector.read_all_topics.assert_called()

    def test_whenSendGameCycleRequest_thenGameCycleConnectorSendsMessage(self):
        self.communication_service.send_game_cycle_response(self.A_MESSAGE)

        self.game_cycle_connector.send_message.assert_called()

    def test_givenGameCycleMessageSentByRobot_whenSendGameCycleRequest_thenGameCycleConnectorReceivesMessage(
        self,
    ):
        self.communication_service.receive_game_cycle_request()

        self.game_cycle_connector.receive_message.assert_called()

    def test_givenAnObject_whenSendObject_thenObjectIsSerializedAndSent(self):
        self.communication_service.send_object(self.A_PATH)

        self.game_cycle_connector.send_object.assert_called_with(self.A_PATH)

    def test_whenReceiveObject_thenObjectIsDeserializedAndReturned(self):
        an_object = MagicMock()
        self.game_cycle_connector.receive_object.return_value = an_object

        actual_object = self.communication_service.receive_object()

        self.assertEqual(an_object, actual_object)
