from typing import Any

from domain.game.Topic import Topic


class Message:
    def __init__(self, topic: Topic, payload: Any):
        self._topic = topic
        self._payload = payload

    def get_topic(self):
        return self._topic

    def get_payload(self):
        return self._payload

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self._topic == other._topic and self._payload == other._payload
