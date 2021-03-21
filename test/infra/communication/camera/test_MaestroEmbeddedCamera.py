from unittest import TestCase
from unittest.mock import MagicMock

from infra.communication.camera.MaestroEmbeddedCamera import MaestroEmbeddedCamera


class TestMaestroEmbeddedCamera(TestCase):
    A_HORIZONTAL_ANGLE_RANGE = (5000, 9000)
    A_VERTICAL_ANGLE_RANGE = (9000, 5000)

    HORIZONTAL_SERVO_ID = 2
    VERTICAL_SERVO_ID = 3

    def setUp(self) -> None:
        self.maestro_controller = MagicMock()
        self.embedded_camera = MaestroEmbeddedCamera(
            self.maestro_controller,
            self.HORIZONTAL_SERVO_ID,
            self.VERTICAL_SERVO_ID,
            self.A_HORIZONTAL_ANGLE_RANGE,
            self.A_VERTICAL_ANGLE_RANGE,
        )

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
