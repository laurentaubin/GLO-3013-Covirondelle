from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    AN_ANGLE = 12

    def setUp(self) -> None:
        self.embedded_camera = MagicMock()
        self.letter_position_extractor = MagicMock()
        self.vision_service = VisionService(
            self.embedded_camera,
            self.letter_position_extractor,
        )

    def test_givenAnAngle_whenRotateCameraHorizontally_thenCameraIsRotated(self):
        self.vision_service.rotate_camera_horizontally(self.AN_ANGLE)

        self.embedded_camera.rotate_horizontally.assert_called_with(self.AN_ANGLE)

    def test_givenAnAngle_whenRotateCameraVertically_thenCameraIsRotated(self):
        self.vision_service.rotate_camera_vertically(self.AN_ANGLE)

        self.embedded_camera.rotate_vertically.assert_called_with(self.AN_ANGLE)

    def test_givenIndex_whenTakeImage_thenImageTaken(self):
        self.vision_service.take_image()

        self.embedded_camera.take_image.assert_called()
