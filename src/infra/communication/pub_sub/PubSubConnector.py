import zmq

from domain.communication.IConnector import IConnector


class PubSubConnector(IConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.SUB)
        self._ping_socket.bind(socket_address)
        self._ping_socket.setsockopt_string(zmq.SUBSCRIBE, "ping")

    def send_message(self, message):
        pass

    def receive_message(self):
        while True:
            topic, message = self._ping_socket.recv().split(maxsplit=1)
            print(topic, message)
