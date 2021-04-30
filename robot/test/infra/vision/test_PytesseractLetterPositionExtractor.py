from unittest import TestCase
from unittest.mock import patch, MagicMock

from infra.vision.CommandPanelPosition import CommandPanelPosition
from infra.vision.PytesseractLetterPositionExtractor import (
    PytesseractLetterPositionExtractor,
)


class TestPytesseractLetterPositionExtractor(TestCase):
    AN_IMAGE = MagicMock()
    PATH_TO_COMMAND_PANEL_IMAGE = "test/infra/vision/panneauCmdZoomed.jpg"
    SECOND_POSITION = CommandPanelPosition.UPPER_RIGHT
    LETTER_D = "D"
    STR_LETTER_LIST = "ABD\nCBC\nADA"
    LETTER_LIST = ["A", "B", "D", "C", "B", "C", "A", "D", "A"]

    @patch("cv2.resize", MagicMock())
    @patch("cv2.cvtColor", MagicMock())
    @patch("cv2.adaptiveThreshold", MagicMock())
    @patch("pytesseract.image_to_string")
    def test_givenAnImage_whenExtractLettersFromImage_ThenLetterReadOnImage(
        self, image_to_string_mock
    ):
        image_to_string_mock.return_value = self.STR_LETTER_LIST
        command_panel_letter_position_extractor = PytesseractLetterPositionExtractor()

        actual_letters = (
            command_panel_letter_position_extractor.extract_letters_from_image(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_letters, self.LETTER_LIST)

    @patch("cv2.resize", MagicMock())
    @patch("cv2.cvtColor", MagicMock())
    @patch("cv2.adaptiveThreshold", MagicMock())
    @patch("pytesseract.image_to_string")
    def test_givenAnImage_whenGetLetterByPosition_ThenReturnLetterAtGivenPosition(
        self, image_to_string_mock
    ):
        image_to_string_mock.return_value = self.STR_LETTER_LIST
        command_panel_letter_position_extractor = PytesseractLetterPositionExtractor()
        command_panel_letter_position_extractor.extract_letters_from_image(
            self.AN_IMAGE
        )

        actual_letter = command_panel_letter_position_extractor.get_letter_by_position(
            self.SECOND_POSITION
        )

        self.assertEqual(self.LETTER_D, actual_letter)
