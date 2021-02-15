from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from config.config import SOCKET_BASE_ADDRESS, PING_PORT
from infra.vision.PuckCenterDetector import PuckCenterDetector
from service.communication.CommunicationService import CommunicationService
from service.vision.VisionService import VisionService


class StationContext:
    def __init__(self):
        self.connector = PubSubConnector(SOCKET_BASE_ADDRESS + PING_PORT)
        self.communication_service = CommunicationService(self.connector)
        self.puck_center_detector = PuckCenterDetector()
        self.vision_service = VisionService(self.puck_center_detector)

    def run(self):
        self.communication_service.send_message()
