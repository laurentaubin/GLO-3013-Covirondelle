from unittest import TestCase
from unittest.mock import Mock, MagicMock

from domain.communication.message import Message
from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = Message("a task", False)

    def setUp(self):
        self.pub_sub_connector = Mock()
        self.game_cycle_connector = Mock()
        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.pub_sub_connector
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
