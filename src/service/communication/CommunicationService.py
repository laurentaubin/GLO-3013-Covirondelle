from typing import Any

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
