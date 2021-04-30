from typing import Tuple

import zmq

from domain.communication.ISubscriberConnector import ISubscriberConnector


class ZmqSubscriberConnector(ISubscriberConnector):
    def __init__(self, socket_address: str):
        self.topics = [
            "gripper_status",
            "power_consumption",
            "first_wheel_power_consumption",
            "second_wheel_power_consumption",
            "third_wheel_power_consumption",
            "fourth_wheel_power_consumption",
            "battery_time_left",
            "battery_percentage",
        ]
        self._socket = self._create_socket(socket_address)
        self._last_information = {key: 0 for key in self.topics}

    def _create_socket(self, socket_address):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.bind(socket_address)
        for topic in self.topics:
            socket.setsockopt_string(zmq.SUBSCRIBE, topic)

        return socket

    def read_all_topics(self) -> Tuple[str, str]:
        topic, message = self._socket.recv_string().split(maxsplit=1)
        return topic, message

    def read_topic(self, topic: str):
        self._update_last_information()
        return self._last_information.get(topic)

    def _update_last_information(self):
        topic, message = self.read_all_topics()

        if topic == "gripper_status":
            if message == "GripperStatus.HAS_PUCK":
                message = 1
            else:
                message = 0
        else:
            message = float(message)

        self._last_information[topic] = message
