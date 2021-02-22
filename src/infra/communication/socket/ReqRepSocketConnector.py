import zmq

from domain.communication.IConnector import IConnector


class ReqRepSocketConnector(IConnector):
    def __init__(self, socket_address):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.bind(socket_address)

    def receive_message(self):
        request_receive = self.socket.recv().decode()
        return request_receive

    def send_message(self, message):
        self.socket.send_string(message)
