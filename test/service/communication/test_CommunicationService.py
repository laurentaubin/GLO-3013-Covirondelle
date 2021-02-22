from unittest import TestCase
from unittest.mock import Mock

from domain.communication.message import Message
from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = Message("a task", False)

    def setUp(self):
        self.pub_sub_connector = Mock()
        self.game_cycle_connector = Mock()
        self.communicationService = CommunicationService(self.game_cycle_connector, self.pub_sub_connector)

    def test_whenReceiveMessage_thenConnectorReceivesMessage(self):
        self.communicationService.receive_game_cycle_message()

        self.assertTrue(self.game_cycle_connector.receive_message.called)

    def test_whenSendMessage_thenConnectorSendsMessage(self):
        self.communicationService.send_game_cycle_message(self.A_MESSAGE)

        self.assertTrue(self.game_cycle_connector.send_message.called_with(self.A_MESSAGE))
