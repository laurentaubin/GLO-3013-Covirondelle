from config.config import SOCKET_ANY_ADDRESS, GAME_CYCLE_PORT
from domain.Position import Position
from domain.pathfinding.Path import Path
from infra.communication.robot.ZmqReqRepConnector import ZmqReqRepConnector

sender_socket = ZmqReqRepConnector(SOCKET_ANY_ADDRESS + GAME_CYCLE_PORT)

path = Path([Position(1, 1), Position(1, 2), Position(1, 3), Position(2, 3)])

sender_socket.send_object(path)
