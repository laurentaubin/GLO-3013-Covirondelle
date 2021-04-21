import cv2
import numpy as np

import GrabPuckIT
from config.config import ROBOT_RADIUS, OBSTACLE_RADIUS, STARTING_ZONE_CENTER_POSITION
from context.StationContext import StationContext
from domain.Color import Color
from domain.Position import Position
from domain.Puck import Puck
from domain.StartingZoneCorner import StartingZoneCorner
from domain.pathfinding.AStarShortestPathAlgorithm import AStarShortestPathAlgorithm
from domain.pathfinding.MazeFactory import MazeFactory
from infra.vision.TemplateMatchingPuckDetector import TemplateMatchingPuckDetector

if __name__ == "__main__":
    context = StationContext(True)
    vision_service = context._vision_service
    table_image, _ = vision_service.get_vision_state()
    second_table_image, _ = vision_service.get_vision_state()
    detector = TemplateMatchingPuckDetector()

    image_width, image_height, _ = table_image.shape
    first_obstacle_position = Position(280, 125)
    second_obstacle_position = Position(402, 184)

    pucks = [
        Puck(color, detector.detect(table_image, color))
        for color in Color
        if color is not Color.NONE
    ]

    maze = MazeFactory(
        ROBOT_RADIUS, OBSTACLE_RADIUS
    ).create_from_shape_and_obstacles_and_pucks_as_obstacles(
        table_image.shape, [first_obstacle_position, second_obstacle_position], pucks
    )

    maze_array = maze._array
    img_to_show = np.zeros((image_width, image_height, 3))

    for i, column in enumerate(maze_array):
        for j, row in enumerate(column):
            if maze_array[i][j] == 1:
                table_image[i][j] = [255, 0, 255]

    cv2.imshow("astar pathfinding algorithm", table_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    corner_pos = (
        vision_service.create_game_table()
        .get_starting_zone()
        .find_corner_position_from_letter(StartingZoneCorner.C)
    )
    maze.add_puck_as_obstacle(corner_pos)
    maze.remove_puck_as_obstacle(pucks[0].get_position())
    print(pucks[0].get_position())

    maze_array = maze._array
    img_to_show = np.zeros((image_width, image_height, 3))

    for i, column in enumerate(maze_array):
        for j, row in enumerate(column):
            if maze_array[i][j] == 1:
                second_table_image[i][j] = [255, 0, 255]

    cv2.imshow("astar pathfinding algorithm", second_table_image)
    cv2.waitKey(0)
