import numpy as np

from domain.Position import Position
from domain.alignment.IAlignmentCorrector import IAlignmentCorrector
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.resistance.ResistanceColor import ResistanceColor
from domain.vision import IPuckDetector


class PuckAlignmentCorrector(IAlignmentCorrector):
    STOP_MOVEMENT = Movement(Direction.STOP, Distance(0))

    def __init__(
        self,
        image_central_point: Position,
        center_position_threshold: int,
        puck_detector: IPuckDetector,
    ):
        self._image_central_point = image_central_point
        self._center_position_threshold = center_position_threshold
        self._puck_detector = puck_detector

    def calculate_horizontal_correction(
        self, image: np.ndarray, puck_color: ResistanceColor
    ) -> Movement:
        puck_position: Position = self._puck_detector.detect(image, puck_color)
        horizontal_distance_from_center: int = (
            puck_position.get_x_coordinate()
            - self._image_central_point.get_x_coordinate()
        )
        if self._is_puck_position_within_horizontal_threshold(
            horizontal_distance_from_center
        ):
            return self.STOP_MOVEMENT
        return self._calculate_horizontal_movement(horizontal_distance_from_center)

    def calculate_vertical_correction(
        self, image: np.ndarray, puck_color: ResistanceColor
    ) -> Movement:
        puck_position: Position = self._puck_detector.detect(image, puck_color)

        vertical_distance_from_center: int = (
            puck_position.get_y_coordinate()
            - self._image_central_point.get_y_coordinate()
        )
        if self._is_puck_within_vertical_threshold(vertical_distance_from_center):
            return self.STOP_MOVEMENT
        return self._calculate_vertical_movement(vertical_distance_from_center)

    def _is_puck_position_within_horizontal_threshold(
        self, horizontal_distance_from_center: int
    ) -> bool:
        return abs(horizontal_distance_from_center) <= self._center_position_threshold

    def _calculate_horizontal_movement(self, distance_from_center: int) -> Movement:
        if self._is_puck_to_the_left(distance_from_center):
            return Movement(Direction.LEFT, Distance(abs(distance_from_center)))
        return Movement(Direction.RIGHT, Distance(distance_from_center))

    def _is_puck_to_the_left(self, distance_from_center: int) -> bool:
        return distance_from_center < 0

    def _calculate_vertical_movement(
        self, vertical_distance_from_center: int
    ) -> Movement:
        if self._is_puck_too_close(vertical_distance_from_center):
            return Movement(
                Direction.BACKWARDS, Distance(vertical_distance_from_center)
            )
        return Movement(Direction.FORWARD, Distance(abs(vertical_distance_from_center)))

    def _is_puck_too_close(self, vertical_distance_from_center: int) -> bool:
        return vertical_distance_from_center > 0

    def _is_puck_within_vertical_threshold(
        self, vertical_distance_from_center: int
    ) -> bool:
        return abs(vertical_distance_from_center) <= self._center_position_threshold
