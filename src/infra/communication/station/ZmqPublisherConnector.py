from threading import Lock
import zmq

from domain.communication.station.IPublisherConnector import IPublisherConnector


class ZmqPublisherConnector(IPublisherConnector):
    def __init__(self, socket_address: str):
        context = zmq.Context()
        self._ping_socket = context.socket(zmq.PUB)
        self._ping_socket.connect(socket_address)
        self.lock = Lock()

    def publish_message(self, message: str) -> None:
        topic = "ping"
        message_data = "Ping pong"
        # self._print_data_to_send(topic, message_data)
        self._ping_socket.send_string("%s %s" % (topic, message_data))

    def _print_data_to_send(self, topic, data):
        self.lock.acquire()
        print("%s %s" % (topic, data))
        self.lock.release()

    def publish_gripper_status(self, gripper_status):
        topic = "gripper_status"
        self._ping_socket.send_string("%s %s" % (topic, str(gripper_status)))

    def publish_power_consumption(self, power_consumption):
        topic = "power_consumption"
        self._ping_socket.send_string("%s %s" % (topic, str(power_consumption)))

    def publish_battery_consumption(self, battery_consumption):
        topic = "battery_consumption"
        self._ping_socket.send_string("%s %s" % (topic, str(battery_consumption)))

    def publish_power_consumption_first_wheel(self, power_consumption_first_wheel):
        topic = "power_consumption_first_wheel"
        self._ping_socket.send_string(
            "%s %s" % (topic, str(power_consumption_first_wheel))
        )

    def publish_power_consumption_second_wheel(self, power_consumption_second_wheel):
        topic = "power_consumption_second_wheel"
        self._ping_socket.send_string(
            "%s %s" % (topic, str(power_consumption_second_wheel))
        )

    def publish_power_consumption_third_wheel(self, power_consumption_third_wheel):
        topic = "power_consumption_third_wheel"
        self._ping_socket.send_string(
            "%s %s" % (topic, str(power_consumption_third_wheel))
        )

    def publish_power_consumption_fourth_wheel(self, power_consumption_fourth_wheel):
        topic = "power_consumption_fourth_wheel"
        self._ping_socket.send_string(
            "%s %s" % (topic, str(power_consumption_fourth_wheel))
        )
