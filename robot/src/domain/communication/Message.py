from typing import Any

from domain.game.Topic import Topic


class Message:
    def __init__(self, topic: Topic, payload: Any):
        self._topic = topic
        self._payload = payload

    def get_topic(self) -> Topic:
        return self._topic

    def get_payload(self) -> Any:
        return self._payload
