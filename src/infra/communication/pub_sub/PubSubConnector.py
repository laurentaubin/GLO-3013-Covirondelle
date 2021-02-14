import zmq

from domain.communication.IConnector import IConnector


class PubSubConnector(IConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.SUB)
        self._ping_socket.connect(socket_address)
        self._ping_socket.setsockopt_string(zmq.SUBSCRIBE, "ping")

    def send_message(self):
        pass

    def receive_message(self):
        for i in range(5):
            topic, message = self._ping_socket.recv().split(maxsplit=1)
            print(topic, message)

    def get_sockets(self):
        return self._ping_socket
