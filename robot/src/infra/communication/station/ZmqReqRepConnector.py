from typing import Any

import zmq

from domain.communication.station.IReqRepConnector import IReqRepConnector


class ZmqReqRepConnector(IReqRepConnector):
    def __init__(self, socket_address):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.bind(socket_address)

    def receive_message(self) -> str:
        return self._socket.recv_string()

    def send_message(self, request: str):
        self._socket.send_string(request)

    def receive_object(self) -> Any:
        print("Receive:")
        message = self._socket.recv_pyobj()
        print(message.get_topic(), message.get_payload())
        return message

    def send_object(self, object_to_send: Any) -> None:
        print("Send:")
        print(object_to_send.get_topic(), object_to_send.get_payload())
        self._socket.send_pyobj(object_to_send)
