import zmq

from domain.communication.ISubscriberConnector import ISubscriberConnector


class ZmqSubscriberConnector(ISubscriberConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.SUB)
        self._ping_socket.bind(socket_address)
        self._ping_socket.setsockopt_string(zmq.SUBSCRIBE, "ping")

    def read_all_topics(self) -> None:
        topic, message = self._ping_socket.recv_string().split(maxsplit=1)
        print(topic, message)
