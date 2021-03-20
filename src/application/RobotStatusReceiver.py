from service.communication.CommunicationService import CommunicationService


class RobotStatusReceiver:
    def __init__(self, communication_service: CommunicationService):
        self.communication_service = communication_service

    def run(self):
        while True:
            self.communication_service.receive_robot_status()
