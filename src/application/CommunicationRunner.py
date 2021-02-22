from service.communication.CommunicationService import CommunicationService


# This class should collect robot information (battery, gripper status, etc. and send all information to station in
# the background)
class CommunicationRunner:
    def __init__(self, communicationService: CommunicationService):
        self.communicationService = communicationService

    def run(self):
        self.communicationService.send_robot_status("ping pong")
