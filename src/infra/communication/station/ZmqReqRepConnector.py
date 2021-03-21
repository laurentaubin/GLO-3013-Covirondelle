from typing import Any

import zmq

from domain.communication.station.IReqRepConnector import IReqRepConnector


class ZmqReqRepConnector(IReqRepConnector):
    def __init__(self, socket_address):
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.connect(socket_address)

    def receive_message(self) -> str:
        return self._socket.recv_string()

    def send_message(self, request: str):
        self._socket.send_string(request)

    def receive_object(self) -> Any:
        return self._socket.recv_pyobj()

    def send_object(self, object_to_send: Any) -> None:
        self._socket.send_pyobj(object_to_send)
