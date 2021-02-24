from domain.communication.IConnector import IConnector


class CommunicationService:
    def __init__(
        self,
        game_cycle_connector: IConnector,
        robot_status_update_connector: IConnector,
    ):
        self.game_cycle_connector = game_cycle_connector
        self.robot_status_update_connector = robot_status_update_connector

    def receive_robot_status(self) -> None:
        self.robot_status_update_connector.receive_message()

    def get_first_corner_letter(self):
        # TODO
        pass

    def receive_game_cycle_request(self):
        return self.game_cycle_connector.receive_message()

    def send_game_cycle_response(self, message):
        self.game_cycle_connector.send_message(message)

    def send_message(self, message) -> None:
        self.robot_status_update_connector.send_message(message)
