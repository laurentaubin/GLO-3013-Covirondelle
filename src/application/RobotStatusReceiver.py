from domain.game.GameState import GameState
from service.communication.CommunicationService import CommunicationService


class RobotStatusReceiver:
    def __init__(self, communication_service: CommunicationService):
        self.communication_service = communication_service

    def run(self):
        while True:
            gripper_state = self.communication_service.receive_gripper_status()
            GameState.get_instance().set_gripper_state(gripper_state)
            battery_consumption = (
                self.communication_service.receive_battery_consumption()
            )
            GameState.get_instance().set_battery_consumption(battery_consumption)
            power_consumption = self.communication_service.receive_power_consumption()
            GameState.get_instance().set_power_consumption(power_consumption)
