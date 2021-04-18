from typing import Any

from domain.communication.IRobotInformation import IRobotInformation
from domain.communication.station.IPublisherConnector import IPublisherConnector
from domain.communication.station.IReqRepConnector import IReqRepConnector


class CommunicationService:
    def __init__(
        self,
        game_cycle_connector: IReqRepConnector,
        pub_sub_connector: IPublisherConnector,
        robot_information: IRobotInformation,
    ):
        self._game_cycle_connector = game_cycle_connector
        self._robot_status_publisher = pub_sub_connector
        self._robot_information = robot_information

    def receive_game_cycle_message(self):
        return self._game_cycle_connector.receive_message()

    def receive_object(self) -> Any:
        return self._game_cycle_connector.receive_object()

    def send_object(self, object_to_send: Any) -> None:
        self._game_cycle_connector.send_object(object_to_send)

    def send_game_cycle_message(self, message) -> None:
        self._game_cycle_connector.send_message(message)

    def send_robot_status(self, message):
        self._robot_status_publisher.publish_message(message)

    def send_gripper_status(self):
        gripper_status = self._robot_information.get_gripper_status()
        self._robot_status_publisher.publish_gripper_status(gripper_status)

    def send_current_consumption(self):
        current_consumption = self._robot_information.get_current_consumption()
        self._robot_status_publisher.publish_current_consumption(current_consumption)

    def send_power_consumption(self):
        power_consumption = self._robot_information.get_power_consumption()
        self._robot_status_publisher.publish_power_consumption(power_consumption)

    def send_power_consumption_first_wheel(self):
        power_consumption_first_wheel = (
            self._robot_information.get_power_consumption_first_wheel()
        )
        self._robot_status_publisher.publish_power_consumption_first_wheel(
            power_consumption_first_wheel
        )

    def send_power_consumption_second_wheel(self):
        power_consumption_second_wheel = (
            self._robot_information.get_power_consumption_second_wheel()
        )
        self._robot_status_publisher.publish_power_consumption_second_wheel(
            power_consumption_second_wheel
        )

    def send_power_consumption_third_wheel(self):
        power_consumption_third_wheel = (
            self._robot_information.get_power_consumption_third_wheel()
        )
        self._robot_status_publisher.publish_power_consumption_third_wheel(
            power_consumption_third_wheel
        )

    def send_power_consumption_fourth_wheel(self):
        power_consumption_fourth_wheel = (
            self._robot_information.get_power_consumption_fourth_wheel()
        )
        self._robot_status_publisher.publish_power_consumption_fourth_wheel(
            power_consumption_fourth_wheel
        )

    def send_battery_time_left(self):
        battery_time_left = self._robot_information.get_battery_time_left()
        self._robot_status_publisher.publish_battery_time_left(battery_time_left)

    def send_battery_percentage(self):
        battery_percentage = self._robot_information.get_battery_percentage()
        self._robot_status_publisher.publish_battery_percentage(battery_percentage)
