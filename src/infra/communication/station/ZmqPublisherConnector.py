import time
from threading import Lock
import zmq

from domain.communication.station.IPublisherConnector import IPublisherConnector


class ZmqPublisherConnector(IPublisherConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.PUB)
        self._ping_socket.connect(socket_address)
        self.lock = Lock()

    def publish_message(self, message: str) -> None:
        while True:
            topic = "ping"
            message_data = "Ping pong"
            # self._print_data_to_send(topic, message_data)
            self._ping_socket.send_string("%s %s" % (topic, message_data))
            time.sleep(1)

    def _print_data_to_send(self, topic, data):
        self.lock.acquire()
        print("%s %s" % (topic, data))
        self.lock.release()
