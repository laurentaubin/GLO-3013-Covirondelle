from unittest import TestCase
from unittest.mock import patch, MagicMock

from infra.vision.CommandPannelPosition import CommandPannelPosition
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)


class TestLetterPositionExtractor(TestCase):
    PATH_TO_COMMAND_PANEL_IMAGE = "test/infra/vision/panneauCmdZoomed.jpg"
    SECOND_POSITION = CommandPannelPosition.UPPER_RIGHT
    LETTER_D = "D"
    STR_LETTER_LIST = "ABD\nCBC\nADA"
    LETTER_LIST = ["A", "B", "D", "C", "B", "C", "A", "D", "A"]

    @patch("cv2.resize", MagicMock())
    @patch("cv2.cvtColor", MagicMock())
    @patch("cv2.adaptiveThreshold", MagicMock())
    @patch("pytesseract.image_to_string")
    def test_givenAnImageWhenReceiveLetterListThenReturnPanelLetterList(
        self, image_to_string_mock
    ):
        image = None

        image_to_string_mock.return_value = self.STR_LETTER_LIST
        command_panel_letter_position_extractor = PytesseractLetterPositionExtractor()
        command_panel_letter_position_extractor.set_command_panel_picture(image)
        list_of_panel_letter = command_panel_letter_position_extractor.get_letter_list()
        self.assertEqual(self.LETTER_LIST, list_of_panel_letter)

    @patch("cv2.resize", MagicMock())
    @patch("cv2.cvtColor", MagicMock())
    @patch("cv2.adaptiveThreshold", MagicMock())
    @patch("pytesseract.image_to_string")
    def test_givenAnImageWhenReceivePositionThenReturnLetterAtGivenPosition(
        self, image_to_string_mock
    ):
        image = None

        image_to_string_mock.return_value = self.STR_LETTER_LIST
        command_panel_letter_position_extractor = PytesseractLetterPositionExtractor()
        command_panel_letter_position_extractor.set_command_panel_picture(image)
        actual_letter = command_panel_letter_position_extractor.get_letter_by_position(
            self.SECOND_POSITION
        )

        self.assertEqual(self.LETTER_D, actual_letter)
