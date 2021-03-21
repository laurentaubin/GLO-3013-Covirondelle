from typing import Any

from domain.communication.station.IPublisherConnector import IPublisherConnector
from domain.communication.station.IReqRepConnector import IReqRepConnector


class CommunicationService:
    def __init__(
        self,
        game_cycle_connector: IReqRepConnector,
        pub_sub_connector: IPublisherConnector,
    ):
        self._game_cycle_connector = game_cycle_connector
        self._robot_status_publisher = pub_sub_connector

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
