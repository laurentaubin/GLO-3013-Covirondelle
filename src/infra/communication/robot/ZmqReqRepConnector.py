from typing import Any

import zmq

from domain.communication.IReqRepConnector import IReqRepConnector


class ZmqReqRepConnector(IReqRepConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.bind(socket_address)

    def receive_message(self) -> str:
        request_receive = self._socket.recv_string()
        return request_receive

    def send_message(self, message: str) -> None:
        self._socket.send_string(message)

    def send_object(self, object_to_send: Any) -> None:
        self._socket.send_pyobj(object_to_send)

    def receive_object(self) -> Any:
        return self._socket.recv_pyobj()
