from unittest import TestCase
from unittest.mock import MagicMock, patch

from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera


class TestOpenCvWorldCamera(TestCase):
    CAMERA_INDEX = 0
    OPENED_SUCCESSFULLY = True
    A_FRAME = MagicMock()
    A_CALIBRATED_IMAGE = MagicMock()

    video_capture = MagicMock()
    camera_calibrator = MagicMock()

    @patch("cv2.VideoCapture")
    def setUp(self, videoCapture_mock) -> None:
        videoCapture_mock.return_value = self.video_capture
        self.world_camera = OpenCvWorldCamera(self.CAMERA_INDEX, self.camera_calibrator)

    def test_whenTakeWorldImage_thenImageIsCalibrated(self):
        self.video_capture.read.return_value = (self.OPENED_SUCCESSFULLY, self.A_FRAME)

        self.world_camera.take_world_image()

        self.camera_calibrator.calibrate.assert_called_with(self.A_FRAME)

    def test_whenTakeWorldImage_thenCalibratedImageIsReturned(self):
        self.video_capture.read.return_value = (self.OPENED_SUCCESSFULLY, self.A_FRAME)
        self.camera_calibrator.calibrate.return_value = self.A_CALIBRATED_IMAGE

        actual_image = self.world_camera.take_world_image()

        self.assertEqual(actual_image, self.A_CALIBRATED_IMAGE)
