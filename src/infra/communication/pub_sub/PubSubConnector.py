import zmq
import time

from domain.communication.IConnector import IConnector


class PubSubConnector(IConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.PUB)
        self._ping_socket.bind(socket_address)

    def send_message(self):
        while True:
            topic = "ping"
            message_data = "Ping pong"
            print("%s %s" % (topic, message_data))
            self._ping_socket.send_string("%s %s" % (topic, message_data))
            time.sleep(1)

    def receive_message(self):
        pass

    def get_sockets(self):
        return self._ping_socket
