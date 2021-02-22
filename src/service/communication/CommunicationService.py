from domain.communication.IConnector import IConnector


class CommunicationService:
    def __init__(self, game_cycle_connector: IConnector, pub_sub_connector: IConnector):
        self.game_cycle_connector = game_cycle_connector
        self.connector = pub_sub_connector

    def receive_game_cycle_message(self):
        return self.game_cycle_connector.receive_message()

    def send_game_cycle_message(self, message) -> None:
        self.game_cycle_connector.send_message(message)

    def send_robot_status(self, message):
        self.connector.send_message(message)
