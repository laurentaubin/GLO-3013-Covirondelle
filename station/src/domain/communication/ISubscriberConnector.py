from typing import Tuple


class ISubscriberConnector:
    def read_all_topics(self) -> Tuple[str, str]:
        pass

    def read_topic(self, topic: str):
        pass
