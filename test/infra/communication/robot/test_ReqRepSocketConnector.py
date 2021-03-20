from unittest import TestCase
from unittest.mock import MagicMock, patch

from infra.communication.robot.ZmqReqRepConnector import ZmqReqRepConnector


class TestZmqReqRepConnector(TestCase):
    A_SOCKET_ADDRESS = "address"
    A_MESSAGE = "message"
    A_SOCKET = MagicMock()

    @patch("zmq.Context.socket", MagicMock(return_value=A_SOCKET))
    def setUp(self) -> None:
        self.zmq_req_rep_connector = ZmqReqRepConnector(self.A_SOCKET_ADDRESS)

    def test_whenSendMessage_thenSocketIsUsedToSendMessage(self):
        self.zmq_req_rep_connector.send_message(self.A_MESSAGE)

        self.A_SOCKET.send_string.assert_called_with(self.A_MESSAGE)

    def test_whenReceiveMessage_thenReturnMessageReceivedBySocket(self):
        self.A_SOCKET.recv_string.return_value = self.A_MESSAGE

        actual_message = self.zmq_req_rep_connector.receive_message()

        self.assertEqual(self.A_MESSAGE, actual_message)

    def test_givenAnObject_whenSendObject_thenSerializeAndSendObjectUsingSocket(self):
        an_object = MagicMock()

        self.zmq_req_rep_connector.send_object(an_object)

        self.A_SOCKET.send_pyobj.assert_called_with(an_object)

    def test_whenReceiveObject_thenDeserializeAndReturnObjectUsingSocket(self):
        an_object = MagicMock()
        self.A_SOCKET.recv_pyobj.return_value = an_object

        actual_object = self.zmq_req_rep_connector.receive_object()

        self.assertEqual(an_object, actual_object)
