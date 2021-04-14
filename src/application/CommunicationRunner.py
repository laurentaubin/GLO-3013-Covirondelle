import time

from service.communication.CommunicationService import CommunicationService


# This class should collect robot information (battery, gripper status, etc. and send all information to station in
# the background)
class CommunicationRunner:
    def __init__(self, communication_service: CommunicationService):
        self._communication_service = communication_service

    def run(self):
        while True:
            self._communication_service.send_gripper_status()
            self._communication_service.send_current_consumption()
            self._communication_service.send_power_consumption()
            time.sleep(1)
