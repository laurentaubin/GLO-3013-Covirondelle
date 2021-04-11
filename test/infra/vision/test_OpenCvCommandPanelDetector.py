from unittest import TestCase
import cv2

from domain.Position import Position
from infra.vision.OpenCvCommandPanelDetector import OpenCvCommandPanelDetector


class TestOpenCvCommandPanelDetector(TestCase):

    AN_IMAGE_WITH_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel.jpg"
    )

    A_ZOOMED_IMAGE_WITH_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_zoomed.jpg"
    )

    AN_IMAGE_FROM_ANGLE_WITH_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_angle.jpg"
    )

    AN_IMAGE_WITH_SMALL_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/small_cmd_panel.JPG"
    )

    A_LEFT_SIDE_IMAGE_OF_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_leftside.JPG"
    )

    A_RIGHT_SIDE_IMAGE_OF_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_rightside.JPG"
    )

    AN_IMAGE_WITH_TOP_OF_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_top.JPG"
    )

    AN_IMAGE_WITH_BOTTOM_OF_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/command_panel_images/cmd_panel_bottom.JPG"
    )

    NOT_A_IMAGE_OF_COMMAND_PANEL = cv2.imread(
        "test/infra/vision/resources/image_with_starting_zone_line.jpg"
    )

    def setUp(self) -> None:
        self._command_panel_detector = OpenCvCommandPanelDetector()

    def test_givenAnImage_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(429, 37)

        actual_position = self._command_panel_detector.detect(
            self.AN_IMAGE_WITH_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAZoomedImage_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(12, 18)

        actual_position = self._command_panel_detector.detect(
            self.A_ZOOMED_IMAGE_WITH_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAnImageWithAngle_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(403, 0)

        actual_position = self._command_panel_detector.detect(
            self.AN_IMAGE_FROM_ANGLE_WITH_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenASmallImage_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(786, 360)

        actual_position = self._command_panel_detector.detect(
            self.AN_IMAGE_WITH_SMALL_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAnImageLeft_side_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(245, 19)

        actual_position = self._command_panel_detector.detect(
            self.A_LEFT_SIDE_IMAGE_OF_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAnImageRight_side_WhenDetect_ThenReturnXEqualZero(
        self,
    ):
        expected_position: Position = Position(0, 27)

        actual_position = self._command_panel_detector.detect(
            self.A_RIGHT_SIDE_IMAGE_OF_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenTheTopOfImage_WhenDetect_ThenReturnTopLeftPanelPosition(
        self,
    ):
        expected_position: Position = Position(249, 23)

        actual_position = self._command_panel_detector.detect(
            self.AN_IMAGE_WITH_TOP_OF_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenTheBottomOfImage_WhenDetect_ThenReturnYEqualZero(
        self,
    ):
        expected_position: Position = Position(241, 0)

        actual_position = self._command_panel_detector.detect(
            self.AN_IMAGE_WITH_BOTTOM_OF_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)

    def test_NotAnImageOfCommandPanel_WhenDetect_ThenReturnOriginEqualZero(
        self,
    ):
        expected_position: Position = Position(0, 0)

        actual_position = self._command_panel_detector.detect(
            self.NOT_A_IMAGE_OF_COMMAND_PANEL
        )

        self.assertEqual(actual_position, expected_position)
