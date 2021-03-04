import cv2
import numpy as np

from domain.Position import Position
from domain.pathfinding.Maze import Maze
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.vision.OpenCvTableDetector import OpenCvTableDetector

if __name__ == "__main__":
    table_image = cv2.imread("../../resources/obstacle3.jpg")
    calibrated_image = OpenCvCalibrator("../../src/config/numpy.npz").calibrate(
        table_image
    )
    cropped_image = OpenCvTableDetector().crop_table(calibrated_image)

    image_width, image_height, _ = cropped_image.shape
    maze = Maze(width=image_width, height=image_height)

    first_obstacle_position = Position(280, 125)
    second_obstacle_position = Position(402, 184)

    maze.add_obstacle(first_obstacle_position)
    maze.add_obstacle(second_obstacle_position)

    maze_array = maze.array
    img_to_show = np.zeros((image_width, image_height, 3))

    for i, column in enumerate(maze_array):
        for j, row in enumerate(column):
            if maze_array[i][j] == 1:
                cropped_image[i][j] = [255, 0, 255]
    cv2.imshow("color test", cropped_image)
    cv2.waitKey(0)
