from typing import Any


class IReqRepConnector:
    def receive_message(self) -> str:
        pass

    def send_message(self, message: str):
        pass

    def receive_object(self) -> Any:
        pass

    def send_object(self, object_to_send: Any) -> None:
        pass
