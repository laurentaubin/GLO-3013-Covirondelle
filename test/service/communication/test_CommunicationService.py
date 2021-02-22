from unittest import TestCase
from unittest.mock import Mock

from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = "a message"
    SOCKET_ADDRESS = "a socket address"

    def setUp(self):
        self.connector = Mock()
        self.robot_update_connector = Mock()
        self.communicationService = CommunicationService(
            self.connector, self.robot_update_connector
        )

    def test_whenReceiveMessage_thenConnectorReceivesMessage(self):
        self.communicationService.receive_robot_status()

        self.assertTrue(self.robot_update_connector.receive_message.called)

    def test_whenSendMessage_thenConnectorSendsMessage(self):
        self.communicationService.send_message(self.A_MESSAGE)

        self.assertTrue(self.robot_update_connector.send_message.called)
