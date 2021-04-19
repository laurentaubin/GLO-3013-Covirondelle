import time

from service.communication.CommunicationService import CommunicationService


# This class should collect robot information (battery, gripper status, etc. and send all information to station in
# the background)
class CommunicationRunner:
    def __init__(self, communication_service: CommunicationService):
        self._communication_service = communication_service

    def run(self):
        while True:
            # self._communication_service.send_gripper_status()
            # self._communication_service.send_current_consumption()
            # self._communication_service.send_power_consumption()
            # self._communication_service.send_power_consumption_first_wheel()
            # self._communication_service.send_power_consumption_second_wheel()
            # self._communication_service.send_power_consumption_third_wheel()
            # self._communication_service.send_power_consumption_fourth_wheel()
            self._communication_service.send_battery_time_left()
            self._communication_service.send_battery_percentage()
            time.sleep(1)
