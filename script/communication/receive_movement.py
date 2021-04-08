import zmq

from config.config import GAME_CYCLE_PORT, SOCKET_STATION_ADDRESS

context = zmq.Context()
receiver_socket = context.socket(zmq.REP)
receiver_socket.connect(SOCKET_STATION_ADDRESS + GAME_CYCLE_PORT)

movements = receiver_socket.recv_pyobj()

for movement in movements:
    print(movement.get_distance().get_distance())
    print(movement.get_direction())
    print()
