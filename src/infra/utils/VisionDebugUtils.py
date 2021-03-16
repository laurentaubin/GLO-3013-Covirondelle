from typing import List

import cv2
import numpy as np

from domain.Position import Position


class VisionDebugUtils:
    @staticmethod
    def show_image(image: np.ndarray) -> None:
        cv2.imshow("debug image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_3D_projection_from_all_image_points(
        img: np.ndarray, all_image_points: List[np.ndarray]
    ) -> np.ndarray:
        for image_points in all_image_points:
            image_points = np.int32(image_points).reshape(-1, 2)

            # draw ground floor in green
            img = cv2.drawContours(img, [image_points[:4]], -1, (0, 255, 0), -3)

            # draw pillars in blue color
            for i, j in zip(range(4), range(4, 8)):
                img = cv2.line(
                    img, tuple(image_points[i]), tuple(image_points[j]), (255), 3
                )

            # draw top layer in red color
            img = cv2.drawContours(img, [image_points[4:]], -1, (0, 0, 255), 3)
        return img

    @staticmethod
    def draw_circle_around_positions(image: np.ndarray, positions: Position) -> None:
        for position in positions:
            cv2.circle(
                image,
                (position.get_x_coordinate(), position.get_y_coordinate()),
                30,
                (0, 0, 255),
                3,
            )
