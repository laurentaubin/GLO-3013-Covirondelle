from unittest import TestCase
from unittest.mock import MagicMock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):
    A_TARGET = 1200
    ANOTHER_TARGET = 1300

    def setUp(self) -> None:
        self.embedded_camera = MagicMock()
        self.letter_position_extractor = MagicMock()
        self.vision_service = VisionService(
            self.embedded_camera,
            self.letter_position_extractor,
            self.A_TARGET,
            self.ANOTHER_TARGET,
        )

    def test_givenTarget_whenRotateCameraHorizontally_thenCameraIsRotated(self):
        self.vision_service.rotate_camera_horizontally(self.A_TARGET)

        self.embedded_camera.rotate_horizontally.assert_called_with(self.A_TARGET)

    def test_givenTarget_whenRotateCameraVertically_thenCameraIsRotated(self):
        self.vision_service.rotate_camera_vertically(self.A_TARGET)

        self.embedded_camera.rotate_vertically.assert_called_with(self.A_TARGET)

    def test_whenMakeCameraLookDown_thenCameraRotatesVerticallyWithLookDownTarget(
        self,
    ):
        self.vision_service.make_camera_look_down()

        self.embedded_camera.rotate_vertically.assert_called_with(self.A_TARGET)

    def test_whenMakeCameraLookUp_thenCameraRotatesVerticallyWithLookUpTarget(
        self,
    ):
        self.vision_service.make_camera_look_up()

        self.embedded_camera.rotate_vertically.assert_called_with(self.ANOTHER_TARGET)

    def test_givenIndex_whenTakeImage_thenImageTaken(self):
        self.vision_service.take_image()

        self.embedded_camera.take_image.assert_called()
