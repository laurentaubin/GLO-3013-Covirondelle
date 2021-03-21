from domain.communication.IEmbeddedCamera import IEmbeddedCamera
from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor


class VisionService:
    def __init__(
        self,
        embedded_camera: IEmbeddedCamera,
        letter_position_extractor: ILetterPositionExtractor,
    ):
        self._embedded_camera = embedded_camera
        self._letter_position_extractor = letter_position_extractor

    def rotate_camera_horizontally(self, angle: float) -> None:
        self._embedded_camera.rotate_horizontally(angle)

    def rotate_camera_vertically(self, angle: float) -> None:
        self._embedded_camera.rotate_vertically(angle)
