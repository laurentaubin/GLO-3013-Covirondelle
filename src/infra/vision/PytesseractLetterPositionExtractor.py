import cv2
import pytesseract


from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor
from infra.vision.CommandPanelPosition import CommandPanelPosition
from config.config import TESSERACT_LOCATION


class PytesseractLetterPositionExtractor(ILetterPositionExtractor):
    def __init__(self):
        self.extracted_letters = []

    def extract_letters_from_image(self, command_panel_image):
        # TODO changer pour le bon path
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_LOCATION
        custom_config = "--psm 11 -c tessedit_char_whitelist=ABCD"

        img = cv2.resize(command_panel_image, None, fx=0.5, fy=0.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adaptive_threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11
        )

        imageText = pytesseract.image_to_string(
            adaptive_threshold, config=custom_config
        )
        self.extracted_letters = list(imageText.replace("\n", ""))

    def get_extracted_letters(
        self,
    ):
        return self.extracted_letters

    def get_letter_by_position(self, letter_position: CommandPanelPosition):
        return self.extracted_letters[letter_position.value]
