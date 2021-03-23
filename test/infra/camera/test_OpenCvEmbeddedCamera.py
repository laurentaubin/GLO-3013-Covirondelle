from unittest import TestCase

from unittest.mock import MagicMock, patch


from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera


class TestOpenCvEmbeddedCamera(TestCase):
    CAMERA_INDEX = 0
    CV2_READ_SUCCESSFULLY = True
    IMAGE_FRAME = MagicMock()
    video_capture = MagicMock()

    @patch("cv2.VideoCapture")
    def setUp(self, videoCapture_mock) -> None:
        videoCapture_mock.return_value = self.video_capture
        self.embedded_camera = OpenCvEmbeddedCamera(self.CAMERA_INDEX)

    def test_whenTakeEmbeddedImage_thenReturnTheCaptured(self):
        self.video_capture.read.return_value = (
            self.CV2_READ_SUCCESSFULLY,
            self.IMAGE_FRAME,
        )

        actual_image = self.embedded_camera.take_image()

        self.assertEqual(actual_image, self.IMAGE_FRAME)
