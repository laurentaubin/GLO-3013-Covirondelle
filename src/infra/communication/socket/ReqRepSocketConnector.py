import zmq

from domain.communication.IConnector import IConnector


class ReqRepSocketConnector(IConnector):
    def __init__(self, socket_address):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.connect(socket_address)

    def receive_message(self):
        message_received = self.socket.recv()

        return message_received.decode()

    def send_message(self, request: str):
        self.socket.send_string(request)
