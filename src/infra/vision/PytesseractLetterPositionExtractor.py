from typing import List

import cv2
import pytesseract

from config.config import TESSERACT_LOCATION
from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor
from infra.vision.CommandPanelPosition import CommandPanelPosition


class PytesseractLetterPositionExtractor(ILetterPositionExtractor):
    DESIRED_LETTERS = ["A", "B", "C", "D"]

    def __init__(self):
        self.extracted_letters = []

    def extract_letters_from_image(self, command_panel_image) -> List[str]:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_LOCATION
        custom_config = "--oem 3 --psm 11 -c tessedit_char_whitelist=ABCD"

        img = cv2.resize(command_panel_image, None, fx=0.7, fy=0.7)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11
        )

        imageText = pytesseract.image_to_string(
            adaptive_threshold, config=custom_config
        )
        self.extracted_letters = list(imageText.replace("\n", ""))
        good_letters = []
        for letter in self.extracted_letters:
            if letter in self.DESIRED_LETTERS:
                good_letters.append(letter)
        self.extracted_letters = good_letters
        print(good_letters)
        return self.extracted_letters

    def get_extracted_letters(
        self,
    ):
        return self.extracted_letters

    def get_letter_by_position(self, letter_position: CommandPanelPosition):
        return self.extracted_letters[letter_position.value]
