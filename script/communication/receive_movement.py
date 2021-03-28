import zmq

from config.config import GAME_CYCLE_PORT, SOCKET_LOCAL_BASE_ADDRESS

context = zmq.Context()
receiver_socket = context.socket(zmq.REP)
receiver_socket.connect(SOCKET_LOCAL_BASE_ADDRESS + GAME_CYCLE_PORT)

movements = receiver_socket.recv_pyobj()

print(movements[0].get_distance().get_distance())
