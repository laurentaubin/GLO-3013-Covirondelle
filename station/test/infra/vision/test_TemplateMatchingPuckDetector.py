import os
from unittest import TestCase

import cv2

from domain.Color import Color
from domain.Position import Position
from infra.vision.TemplateMatchingPuckDetector import TemplateMatchingPuckDetector


class TestTemplateMatchingPuckDetector(TestCase):
    AN_IMAGE_PATH = (
        os.path.dirname(os.path.abspath(__file__))
        + "/../../../resources/camera-config/image_0.jpg"
    )
    AN_IMAGE = cv2.imread(AN_IMAGE_PATH)

    def setUp(self) -> None:
        self.template_matching_puck_detector = TemplateMatchingPuckDetector()

    def test_givenColorGrey_whenDetect_thenReturnRightPositionForGreyPuck(self):
        expected_position = Position(1181, 192)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.GREY
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorRed_whenDetect_thenReturnRightPositionForRedPuck(self):
        expected_position = Position(1184, 335)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.RED
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorGreen_whenDetect_thenReturnRightPositionForGreenPuck(self):
        expected_position = Position(1078, 182)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.GREEN
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorYellow_whenDetect_thenReturnRightPositionForYellowPuck(self):
        expected_position = Position(967, 632)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.YELLOW
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorOrange_whenDetect_thenReturnRightPositionForOrangePuck(self):
        expected_position = Position(888, 636)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.ORANGE
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorBlue_whenDetect_thenReturnRightPositionForBluePuck(self):
        expected_position = Position(1072, 626)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.BLUE
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorPurple_whenDetect_thenReturnRightPositionForPurplePuck(self):
        expected_position = Position(1155, 625)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.PURPLE
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorWhite_whenDetect_thenReturnRightPositionForWhitePuck(self):
        expected_position = Position(902, 175)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.WHITE
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorBrown_whenDetect_thenReturnRightPositionForBrownPuck(self):
        expected_position = Position(985, 180)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.BROWN
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenColorBlack_whenDetect_thenReturnRightPositionForBlackPuck(self):
        expected_position = Position(1175, 489)

        actual_position = self.template_matching_puck_detector.detect(
            self.AN_IMAGE, Color.BLACK
        )

        self.assertEqual(actual_position, expected_position)

    def test_givenAnImage_whenDetectAllColors_thenColorsAllHaveDifferentPositions(self):
        possible_colors = []
        for color in Color:
            if color is not Color.NONE:
                possible_colors.append(color)

        color_positions = [
            self.template_matching_puck_detector.detect(self.AN_IMAGE, color)
            for color in possible_colors
        ]

        different_positions = set(color_positions)
        self.assertEqual(len(different_positions), 10)
