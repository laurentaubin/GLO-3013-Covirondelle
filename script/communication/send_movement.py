from unittest.mock import MagicMock

import cv2

from application.ApplicationServer import ApplicationServer
from context.StationContext import StationContext
from domain.Position import Position
from domain.game.GameState import GameState
from domain.movement.MovementFactory import MovementFactory


class TestContext(StationContext):
    def __init__(self):
        super().__init__(local_flag=False)


if __name__ == "__main__":
    context = TestContext()
    server = ApplicationServer(
        MagicMock(), MagicMock(), context._vision_worker, MagicMock()
    )
    server.run()

    input("Ready to start, press enter to continue")

    game_table = context._vision_service.create_game_table()
    context._path_service.set_game_table(game_table)

    puck_position = Position(1400, 600)
    path = (
        context._shortest_path_algorithm.find_shortest_path_with_cartesian_coordinates(
            GameState.get_instance().get_robot_pose().get_position(), puck_position
        )
    )

    movement_factory = MovementFactory()
    movements = movement_factory.create_movements(path)
    maze_array = context._vision_service.create_game_table().get_maze()

    table_image = context._world_camera.take_world_image()

    for i, column in enumerate(maze_array):
        for j, row in enumerate(column):
            if maze_array[i][j] == 1:
                table_image[i][j] = [255, 0, 255]

    for element in path:
        table_image[element.get_y_coordinate()][element.get_x_coordinate()] = [
            0,
            255,
            0,
        ]

    cv2.imshow("astar pathfinding algorithm", table_image)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

    print("sending movement")
    for movement in movements:
        print(movement.get_direction())
    # context._communication_service.send_object(movements)
    print("movement sent")
