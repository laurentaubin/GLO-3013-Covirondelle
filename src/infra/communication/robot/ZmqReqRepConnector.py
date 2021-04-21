from typing import Any

import zmq

from domain.communication.IReqRepConnector import IReqRepConnector


class ZmqReqRepConnector(IReqRepConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.connect(socket_address)

    def receive_message(self) -> str:
        request_receive = self._socket.recv_string()
        return request_receive

    def send_message(self, message: str) -> None:
        self._socket.send_string(message)

    def receive_object(self) -> Any:
        print("Receive:")
        message = self._socket.recv_pyobj()
        print(message.get_topic(), message.get_payload())
        return message

    def send_object(self, object_to_send: Any) -> None:
        print("Send:")
        print(object_to_send.get_topic(), object_to_send.get_payload())
        self._socket.send_pyobj(object_to_send)
