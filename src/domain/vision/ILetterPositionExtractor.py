from typing import List

import numpy as np


class ILetterPositionExtractor:
    def extract_letters_from_image(self, command_panel_image: np.ndarray) -> None:
        pass

    def get_extracted_letters(self) -> List[str]:
        pass

    def get_letter_by_position(self, position: int):
        pass
