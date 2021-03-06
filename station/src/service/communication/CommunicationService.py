from typing import Any

from domain.communication.GripperStatus import GripperStatus
from domain.communication.IReqRepConnector import IReqRepConnector
from domain.communication.ISubscriberConnector import ISubscriberConnector


class CommunicationService:
    def __init__(
        self,
        game_cycle_connector: IReqRepConnector,
        robot_status_update_connector: ISubscriberConnector,
    ):
        self._game_cycle_connector = game_cycle_connector
        self._robot_status_update_connector = robot_status_update_connector

    def receive_robot_status(self) -> None:
        self._robot_status_update_connector.read_all_topics()

    def receive_game_cycle_request(self):
        return self._game_cycle_connector.receive_message()

    def send_game_cycle_response(self, message):
        self._game_cycle_connector.send_message(message)

    def send_object(self, obj: Any):
        self._game_cycle_connector.send_object(obj)

    def receive_object(self):
        return self._game_cycle_connector.receive_object()

    def receive_gripper_status(self) -> GripperStatus:
        gripper_status = self._robot_status_update_connector.read_topic(
            "gripper_status"
        )
        return GripperStatus.valueOf(gripper_status)

    def receive_power_consumption(self) -> float:
        return self._robot_status_update_connector.read_topic("power_consumption")

    def receive_battery_consumption(self) -> float:
        return self._robot_status_update_connector.read_topic("battery_consumption")

    def receive_battery_time_left(self) -> float:
        return self._robot_status_update_connector.read_topic("battery_time_left")

    def receive_battery_percentage(self) -> float:
        return self._robot_status_update_connector.read_topic("battery_percentage")

    def receive_power_consumption_first_wheel(self) -> float:
        return self._robot_status_update_connector.read_topic(
            "first_wheel_power_consumption"
        )

    def receive_power_consumption_second_wheel(self) -> float:
        return self._robot_status_update_connector.read_topic(
            "second_wheel_power_consumption"
        )

    def receive_power_consumption_third_wheel(self) -> float:
        return self._robot_status_update_connector.read_topic(
            "third_wheel_power_consumption"
        )

    def receive_power_consumption_fourth_wheel(self) -> float:
        return self._robot_status_update_connector.read_topic(
            "fourth_wheel_power_consumption"
        )
