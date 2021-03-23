from domain.IEmbeddedCamera import IEmbeddedCamera
from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor


class VisionService:
    def __init__(
        self,
        embedded_camera: IEmbeddedCamera,
        letter_position_extractor: ILetterPositionExtractor,
        robot_embedded_camera: IEmbeddedCamera,
    ):
        self._embedded_camera = embedded_camera
        self._letter_position_extractor = letter_position_extractor
        self._robot_embedded_camera = robot_embedded_camera

    def rotate_camera_horizontally(self, angle: float) -> None:
        self._embedded_camera.rotate_horizontally(angle)

    def rotate_camera_vertically(self, angle: float) -> None:
        self._embedded_camera.rotate_vertically(angle)

    def take_image(self):
        self._robot_embedded_camera.take_image()
