from unittest.mock import MagicMock

import cv2
import os

from domain.Color import Color
from integration.IntegrationContext import IntegrationContext


class PuckDetectionIt(IntegrationContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)
        self.images = []
        self._setup_vision_service()

    def _setup_vision_service(self):
        self._vision_service._calibrator = MagicMock()
        self.image_paths = self._find_files_in_directory("../resources/test/puck")
        for image_path in self.image_paths:
            self.images.append(cv2.imread(image_path))
        number_of_colors_to_detect = len(Color) - 1
        self._vision_service._calibrator.calibrate.side_effect = [
            item
            for sublist in [[elem] * number_of_colors_to_detect for elem in self.images]
            for item in sublist
        ]

    def run(self):
        for i, image in enumerate(self.image_paths):
            print(f"Detecting pucks on image {image}")
            self._detect_pucks_in_image(i)
            cv2.imshow(f"Test {self.image_paths[i]}", self.images[i])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print()

    def _find_files_in_directory(self, directory):
        files = []
        for file in os.listdir(directory):
            files.append(f"{directory}/{file}")
        return files

    def _detect_pucks_in_image(self, iteration_number: int):
        successes = []
        failures = []
        for color in Color:
            if color is Color.NONE:
                continue
            try:
                puck_position = self._vision_service.find_puck_position(color)
                successes.append((color, puck_position))
            except Exception as e:
                failures.append(color)
                print(e)

        for success in successes:
            color, puck_position = success
            print(
                f"Successfully detected puck {color.name} at position {puck_position}"
            )
            self._annotate_image(color, iteration_number, puck_position)

        for color in failures:
            print(f"Unsuccessfully detected puck {color.name}")

    def _annotate_image(self, color, iteration_number, puck_position):
        cv2.circle(
            self.images[iteration_number],
            puck_position.to_tuple(),
            25,
            (0, 255, 0),
            1,
        )
        text_position = (
            puck_position.get_x_coordinate() - 50,
            puck_position.get_y_coordinate() - 40,
        )
        cv2.putText(
            self.images[iteration_number],
            color.name,
            text_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            20,
        )


if __name__ == "__main__":
    puck_detection_it = PuckDetectionIt(local_flag=True)

    puck_detection_it.run()
