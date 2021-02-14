from domain.communication.IConnector import IConnector


class CommunicationService:
    def __init__(self, connector: IConnector):
        self.connector = connector

    def receive_message(self) -> None:
        self.connector.receive_message()

    def send_message(self) -> None:
        self.connector.send_message()
