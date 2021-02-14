from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from config.config import SOCKET_BASE_ADDRESS, PING_PORT
from service.communication.CommunicationService import CommunicationService


class RobotContext:
    def __init__(self):
        self.connector = PubSubConnector(SOCKET_BASE_ADDRESS + PING_PORT)
        self.communication_service = CommunicationService(self.connector)

    def run(self):
        self.communication_service.receive_message()
