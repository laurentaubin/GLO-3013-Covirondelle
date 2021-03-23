from unittest import TestCase

from unittest.mock import MagicMock, patch


from infra.camera.OpenCvEmbeddedCamera import OpenCvEmbeddedCamera


class TestOpenCvEmbeddedCamera(TestCase):
    CAMERA_INDEX = 0
    CV2_READ_SUCCESSFULLY = True
    IMAGE_FRAME = MagicMock()
    A_HORIZONTAL_ANGLE_RANGE = (5000, 9000)
    A_VERTICAL_ANGLE_RANGE = (9000, 5000)

    HORIZONTAL_SERVO_ID = 2
    VERTICAL_SERVO_ID = 3

    video_capture = MagicMock()
    maestro_controller = MagicMock()

    @patch("cv2.VideoCapture", MagicMock(return_value=video_capture))
    def setUp(self) -> None:
        self.embedded_camera = OpenCvEmbeddedCamera(
            self.CAMERA_INDEX,
            self.maestro_controller,
            self.HORIZONTAL_SERVO_ID,
            self.VERTICAL_SERVO_ID,
            self.A_HORIZONTAL_ANGLE_RANGE,
            self.A_VERTICAL_ANGLE_RANGE,
        )

    def test_whenTakeEmbeddedImage_thenReturnTheCaptured(self):
        self.video_capture.read.return_value = (
            self.CV2_READ_SUCCESSFULLY,
            self.IMAGE_FRAME,
        )

        actual_image = self.embedded_camera.take_image()

        self.assertEqual(actual_image, self.IMAGE_FRAME)

    def test_givenARotationAngle_whenRotateHorizontally_thenMaestroControllerRotatesHorizontalServo(
        self,
    ):
        an_angle = 90
        expected_target = 6000.0

        self.embedded_camera.rotate_horizontally(an_angle)

        self.maestro_controller.setTarget.assert_called_with(
            self.HORIZONTAL_SERVO_ID, expected_target
        )

    def test_givenARotationAngle_whenRotateVertically_thenMaestroControllerRotatesVerticalServo(
        self,
    ):
        an_angle = 45
        expected_target = 8500.0

        self.embedded_camera.rotate_vertically(an_angle)

        self.maestro_controller.setTarget.assert_called_with(
            self.VERTICAL_SERVO_ID, expected_target
        )
