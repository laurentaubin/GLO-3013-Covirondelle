from unittest import TestCase
from unittest.mock import patch
import numpy as np

from domain.Position import Position
from domain.StartingZone import StartingZone
from infra.vision.OpenCvCornerDetector import OpenCvCornerDetector


class TestOpenCvCornerDetector(TestCase):
    def setUp(self) -> None:
        self.detector = OpenCvCornerDetector()

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    def test_givenFourPointsInsideStartingZoneRange_whenDetect_thenAllFourPointsAreReturned(
        self, goodFeaturesToTrack_mock, _cvtColor_mock
    ):
        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231]]
        )
        expected_coordinates = [
            Position(627, 233),
            Position(620, 666),
            Position(227, 650),
            Position(225, 231),
        ]
        expected_starting_corner = StartingZone(expected_coordinates)

        actual_starting_corner = self.detector.detect_starting_zone(board_image)

        self.assertEqual(expected_starting_corner, actual_starting_corner)

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    def test_givenPointsInsideAndOutsideStartingZoneRange_whenDetect_thenOnlyPointsInsideStartingZoneRangeAreReturned(
        self, goodFeaturesToTrack_mock, _cvtColor_mock
    ):
        board_image = np.array([])
        all_coordinates = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231], [1033, 5642], [6541, 213]]
        )
        goodFeaturesToTrack_mock.return_value = all_coordinates
        expected_coordinates = [
            Position(627, 233),
            Position(620, 666),
            Position(227, 650),
            Position(225, 231),
        ]
        expected_starting_corner = StartingZone(expected_coordinates)

        actual_starting_corner = self.detector.detect_starting_zone(board_image)

        self.assertEqual(expected_starting_corner, actual_starting_corner)
