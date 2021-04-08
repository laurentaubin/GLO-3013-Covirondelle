from domain.camera.IEmbeddedCamera import IEmbeddedCamera
from domain.vision.ILetterPositionExtractor import ILetterPositionExtractor


class VisionService:
    def __init__(
        self,
        embedded_camera: IEmbeddedCamera,
        letter_position_extractor: ILetterPositionExtractor,
        camera_look_down_target: int,
        camera_look_up_target: int,
    ):
        self._embedded_camera = embedded_camera
        self._letter_position_extractor = letter_position_extractor
        self._camera_look_down_target = camera_look_down_target
        self._camera_look_up_target = camera_look_up_target

    def rotate_camera_horizontally(self, target: int) -> None:
        self._embedded_camera.rotate_horizontally(target)

    def rotate_camera_vertically(self, target: int) -> None:
        self._embedded_camera.rotate_vertically(target)

    def make_camera_look_down(self) -> None:
        self._embedded_camera.rotate_vertically(self._camera_look_down_target)

    def make_camera_look_up(self) -> None:
        self._embedded_camera.rotate_vertically(self._camera_look_up_target)

    def take_image(self):
        return self._embedded_camera.take_image()
