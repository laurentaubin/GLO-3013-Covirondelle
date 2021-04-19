import time
from unittest.mock import MagicMock

from config.config import GAME_CYCLE_PORT, SOCKET_LOCAL_BASE_ADDRESS, PING_PORT
from infra.communication.robot_information.StmRobotInformation import (
    StmRobotInformation,
)
from infra.communication.station.ZmqPublisherConnector import ZmqPublisherConnector
from infra.communication.station.ZmqReqRepConnector import ZmqReqRepConnector
from service.communication.CommunicationService import CommunicationService


serial = MagicMock()

game_cycle_connector = ZmqReqRepConnector(SOCKET_LOCAL_BASE_ADDRESS + GAME_CYCLE_PORT)
publisher_connector = ZmqPublisherConnector(SOCKET_LOCAL_BASE_ADDRESS + PING_PORT)

robot_information = StmRobotInformation(serial)

communication_service = CommunicationService(
    game_cycle_connector, publisher_connector, robot_information
)

serial.write_and_readline.return_value = bytes("8", encoding="utf-8") + bytes(
    "400", encoding="utf-8"
)

for i in range(5):
    print("send grip")
    communication_service.send_gripper_status()
    time.sleep(0.5)

serial.write_and_readline.return_value = bytes("8", encoding="utf-8") + bytes(
    "400", encoding="utf-8"
)

for i in range(5):
    communication_service.send_gripper_status()
    time.sleep(0.5)
