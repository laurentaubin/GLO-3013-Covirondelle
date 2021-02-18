from infra.communication.pub_sub.PubSubConnector import PubSubConnector
from config.config import SOCKET_BASE_ADDRESS, PING_PORT
from infra.vision.OpenCvPuckCenterDetector import OpenCvPuckCenterDetector
from infra.vision.OpenCvSCornerDetector import (
    OpenCvCornerDetector,
)
from service.communication.CommunicationService import CommunicationService
from service.vision.VisionService import VisionService


class StationContext:
    def __init__(self):
        connector = PubSubConnector(SOCKET_BASE_ADDRESS + PING_PORT)
        self.communication_service = CommunicationService(connector)
        puck_center_detector = OpenCvPuckCenterDetector()
        starting_zone_corners_detector = OpenCvCornerDetector()
        self.vision_service = VisionService(
            puck_center_detector, starting_zone_corners_detector
        )

    def run(self):
        self.communication_service.send_message()
