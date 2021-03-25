import zmq

from domain.communication.ISubscriberConnector import ISubscriberConnector


class ZmqSubscriberConnector(ISubscriberConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.bind(socket_address)
        self._socket.setsockopt_string(zmq.SUBSCRIBE, "ping")
        self._socket.setsockopt_string(zmq.SUBSCRIBE, "gripper_status")

    def read_all_topics(self) -> None:
        topic, message = self._socket.recv_string().split(maxsplit=1)
        print(topic, message)
