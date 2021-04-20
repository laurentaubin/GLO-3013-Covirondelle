import time

from domain.game.GameState import GameState
from service.communication.CommunicationService import CommunicationService


class RobotStatusReceiver:
    def __init__(self, communication_service: CommunicationService):
        self.communication_service = communication_service

    def run(self):
        while True:
            gripper_state = self.communication_service.receive_gripper_status()
            GameState.get_instance().set_gripper_state(gripper_state)
            battery_time_left = self.communication_service.receive_battery_time_left()
            battery_percentage = self.communication_service.receive_battery_percentage()
            power_consumption_first_wheel = (
                self.communication_service.receive_power_consumption_first_wheel()
            )
            power_consumption_second_wheel = (
                self.communication_service.receive_power_consumption_second_wheel()
            )
            power_consumption_third_wheel = (
                self.communication_service.receive_power_consumption_third_wheel()
            )
            power_consumption_fourth_wheel = (
                self.communication_service.receive_power_consumption_fourth_wheel()
            )
            power_consumption = self.communication_service.receive_power_consumption()
            GameState.get_instance().set_battery_consumption(power_consumption)
            GameState.get_instance().set_battery_time_left(battery_time_left)
            GameState.get_instance().set_battery_percentage(battery_percentage)
            GameState.get_instance().set_power_consumption_first_wheel(
                power_consumption_first_wheel
            )
            GameState.get_instance().set_power_consumption_second_wheel(
                power_consumption_second_wheel
            )
            GameState.get_instance().set_power_consumption_third_wheel(
                power_consumption_third_wheel
            )
            GameState.get_instance().set_power_consumption_fourth_wheel(
                power_consumption_fourth_wheel
            )
            time.sleep(1)
