from config.config import SOCKET_ROBOT_ADDRESS, PING_PORT
from infra.communication.robot.ZmqSubscriberConnector import ZmqSubscriberConnector

sub = ZmqSubscriberConnector(SOCKET_ROBOT_ADDRESS + PING_PORT)

for i in range(10):
    sub.read_all_topics()
