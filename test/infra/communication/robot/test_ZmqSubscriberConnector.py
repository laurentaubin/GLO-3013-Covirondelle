from unittest import TestCase
from unittest.mock import patch, MagicMock

from infra.communication.robot.ZmqSubscriberConnector import ZmqSubscriberConnector


class TestZmqSubscriberConnector(TestCase):
    A_SOCKET_ADDRESS = "address"
    A_MESSAGE = "topic message"
    A_SOCKET = MagicMock()

    @patch("zmq.Context.socket", MagicMock(return_value=A_SOCKET))
    def setUp(self) -> None:
        self.zmq_subscriber_connector = ZmqSubscriberConnector(self.A_SOCKET_ADDRESS)

    def test_whenReadAllTopics_thenSocketReadsChannel(self):
        self.A_SOCKET.recv_string.return_value = self.A_MESSAGE

        self.zmq_subscriber_connector.read_all_topics()

        self.A_SOCKET.recv_string.assert_called()
