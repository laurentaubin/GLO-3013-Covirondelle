from unittest import TestCase
from unittest.mock import patch, MagicMock
import numpy as np

from domain.Position import Position

from infra.vision.OpenCvStartingZoneDetector import (
    OpenCvStartingZoneDetector,
    StartingZoneCornersNotFound,
    StartingZoneCenterNotFound,
    StartingZoneCenterDetectedOutsideStartingZone,
)


class TestOpenCvCornerDetector(TestCase):
    STARTING_ZONE_CENTER = Position(426, 449)
    A_LIST_OF_CONTOURS = [1]
    A_HIERARCHY = 8
    A_LIST_OF_CORNERS = [[627, 233], [620, 666], [227, 650], [225, 231]]
    STARTING_ZONE_CENTER_OUT_OF_BOUND = Position(0, 0)
    A_BOARD_IMAGE = np.array([])
    AREA_SMALLER_THAN_THRESHOLD = 8000
    AREA_GREATER_THAN_THRESHOLD = 9500

    def setUp(self) -> None:
        self.detector = OpenCvStartingZoneDetector()

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.moments")
    @patch("cv2.findContours")
    @patch("cv2.GaussianBlur")
    @patch("cv2.Canny")
    def test_givenFourPointsInsideStartingZoneRange_whenDetect_thenAllFourPointsAreReturned(
        self,
        Canny_mock,
        GaussianBlur_mock,
        findContours_mock,
        moments_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
    ):
        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231]]
        )
        expected_coordinates = [
            Position(225, 231),
            Position(627, 233),
            Position(227, 650),
            Position(620, 666),
        ]
        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_GREATER_THAN_THRESHOLD
        moments_mock.return_value = {
            "m00": 1,
            "m10": self.STARTING_ZONE_CENTER.get_x_coordinate(),
            "m01": self.STARTING_ZONE_CENTER.get_y_coordinate(),
        }

        actual_starting_zone = self.detector.detect(board_image)

        self.assertEqual(expected_coordinates, actual_starting_zone.get_corners())

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.moments")
    @patch("cv2.findContours")
    @patch("cv2.GaussianBlur")
    @patch("cv2.Canny")
    def test_givenPointsInsideAndOutsideStartingZoneRange_whenDetect_thenOnlyPointsInsideStartingZoneRangeAreReturned(
        self,
        Canny_mock,
        GaussianBlur_mock,
        findContours_mock,
        moments_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
    ):
        board_image = np.array([])
        all_coordinates = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231], [1033, 5642], [6541, 213]]
        )
        goodFeaturesToTrack_mock.return_value = all_coordinates
        expected_coordinates = [
            Position(225, 231),
            Position(627, 233),
            Position(227, 650),
            Position(620, 666),
        ]
        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_GREATER_THAN_THRESHOLD
        moments_mock.return_value = {
            "m00": 1,
            "m10": self.STARTING_ZONE_CENTER.get_x_coordinate(),
            "m01": self.STARTING_ZONE_CENTER.get_y_coordinate(),
        }

        actual_starting_corner = self.detector.detect(board_image)

        self.assertEqual(expected_coordinates, actual_starting_corner.get_corners())

    @patch("cv2.Canny")
    @patch("cv2.GaussianBlur")
    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.findContours")
    def test_givenListOfPointsNotEqualToFour_whenDetect_thenThrowsStartingZoneCornersNotFound(
        self,
        findContours_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
        GaussianBlur_mock,
        Canny_mock,
    ):
        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650]]
        )

        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_GREATER_THAN_THRESHOLD

        with self.assertRaises(StartingZoneCornersNotFound):
            self.detector.detect(board_image)

    @patch("cv2.Canny")
    @patch("cv2.GaussianBlur")
    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.findContours")
    def test_givenWrongMinimumArea_whenDetect_thenThrowsStartingZoneCenterNotFound(
        self,
        findContours_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
        GaussianBlur_mock,
        Canny_mock,
    ):
        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231]]
        )

        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_SMALLER_THAN_THRESHOLD

        with self.assertRaises(StartingZoneCenterNotFound):
            self.detector.detect(board_image)

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.moments")
    @patch("cv2.findContours")
    @patch("cv2.GaussianBlur")
    @patch("cv2.Canny")
    def test_givenFourPointsInsideStartingZoneRange_whenDetect_thenOnlyOnePointInTheZoneIsReturned(
        self,
        Canny_mock,
        GaussianBlur_mock,
        findContours_mock,
        moments_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
    ):

        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231]]
        )
        expected_center = self.STARTING_ZONE_CENTER

        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_GREATER_THAN_THRESHOLD
        moments_mock.return_value = {
            "m00": 1,
            "m10": self.STARTING_ZONE_CENTER.get_x_coordinate(),
            "m01": self.STARTING_ZONE_CENTER.get_y_coordinate(),
        }

        actual_starting_zone_center = self.detector.detect(board_image).get_center()

        self.assertEqual(expected_center, actual_starting_zone_center)

    @patch("cv2.cvtColor")
    @patch("cv2.goodFeaturesToTrack")
    @patch("cv2.contourArea")
    @patch("cv2.moments")
    @patch("cv2.findContours")
    @patch("cv2.GaussianBlur")
    @patch("cv2.Canny")
    def test_givenACenterOutsideStartingZone_whenDetect_thenThrowStartingZoneCenterDetectedOutsideStartingZone(
        self,
        Canny_mock,
        GaussianBlur_mock,
        findContours_mock,
        moments_mock,
        contourArea_mock,
        goodFeaturesToTrack_mock,
        cvtColor_mock,
    ):
        board_image = np.array([])
        goodFeaturesToTrack_mock.return_value = np.array(
            [[627, 233], [620, 666], [227, 650], [225, 231]]
        )
        findContours_mock.return_value = (self.A_LIST_OF_CONTOURS, self.A_HIERARCHY)
        contourArea_mock.return_value = self.AREA_GREATER_THAN_THRESHOLD
        moments_mock.return_value = {
            "m00": 1,
            "m10": self.STARTING_ZONE_CENTER.get_x_coordinate(),
            "m01": self.STARTING_ZONE_CENTER.get_y_coordinate(),
        }

        self.detector._detect_starting_zone_center = MagicMock(
            return_value=self.STARTING_ZONE_CENTER_OUT_OF_BOUND
        )

        with self.assertRaises(StartingZoneCenterDetectedOutsideStartingZone):
            self.detector.detect(board_image)
