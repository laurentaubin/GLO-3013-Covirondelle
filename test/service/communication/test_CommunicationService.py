from unittest import TestCase
from unittest.mock import Mock

from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    SOCKET_ADDRESS = "a socket address"

    def setUp(self):
        self.connector = Mock()
        self.communicationService = CommunicationService(self.connector)

    def test_whenReceiveMessage_thenConnectorReceivesMessage(self):
        self.communicationService.receive_message()

        self.assertTrue(self.connector.receive_message.called)

    def test_whenSendMessage_thenConnectorSendsMessage(self):
        self.communicationService.send_message()

        self.assertTrue(self.connector.send_message.called)
