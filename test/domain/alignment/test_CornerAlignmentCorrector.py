from unittest import TestCase
from unittest.mock import MagicMock

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.alignment.CornerAlignmentCorrector import CornerAlignmentCorrector
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed


class TestCornerAlignmentCorrector(TestCase):
    ALIGNED_POSITION = Position(340, 300)
    CORNER_TOO_MUCH_THE_RIGHT = Position(380, 300)
    CORNER_TOO_MUCH_THE_LEFT = Position(300, 300)
    CORNER_TOO_MUCH_FORWARD = Position(340, 200)
    AN_IMAGE = MagicMock()

    def setUp(self) -> None:
        self.corner_detector = MagicMock()
        self.corner_alignment_corrector = CornerAlignmentCorrector(
            self.corner_detector, self.ALIGNED_POSITION
        )

    def test_givenAnImage_whenCalculateHorizontalAlignment_thenInferiorCornerIsDetectedFromImage(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = self.ALIGNED_POSITION

        self.corner_alignment_corrector.calculate_horizontal_correction(self.AN_IMAGE)

        self.corner_detector.detect_inferior_corner.assert_called_with(self.AN_IMAGE)

    def test_givenAlreadyAlignedHorizontally_whenCalculateHorizontalCorrection_thenReturnStopMovementCommand(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = self.ALIGNED_POSITION
        expected_movement_command = MovementCommand(
            Direction.STOP, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )

        actual_movement_command = (
            self.corner_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement_command, expected_movement_command)

    def test_givenCornerTooMuchOnTheRight_whenCalculateHorizontalCorrection_thenReturnRightMovementCommand(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = (
            self.CORNER_TOO_MUCH_THE_RIGHT
        )
        expected_movement_command = MovementCommand(
            Direction.RIGHT, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )

        actual_movement_command = (
            self.corner_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement_command, expected_movement_command)

    def test_givenCornerTooMuchOnTheLeft_whenCalculateHorizontalCorrection_thenReturnLeftMovementCommand(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = (
            self.CORNER_TOO_MUCH_THE_LEFT
        )
        expected_movement_command = MovementCommand(
            Direction.LEFT, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )

        actual_movement_command = (
            self.corner_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement_command, expected_movement_command)

    def test_givenAnImage_whenCalculateVerticalAlignment_thenInferiorCornerIsDetectedFromImage(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = self.ALIGNED_POSITION

        self.corner_alignment_corrector.calculate_vertical_correction(self.AN_IMAGE)

        self.corner_detector.detect_inferior_corner.assert_called_with(self.AN_IMAGE)

    def test_givenCorrectlyAlignedVertically_whenCalculateVerticalCorrection_thenReturnStopMovementCommand(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = self.ALIGNED_POSITION
        expected_movement_command = MovementCommand(
            Direction.STOP, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )

        actual_movement_command = (
            self.corner_alignment_corrector.calculate_vertical_correction(self.AN_IMAGE)
        )

        self.assertEqual(actual_movement_command, expected_movement_command)

    def test_givenCornerTooMuchForward_whenCalculateVerticalCorrection_thenReturnForwardMovementCommand(
        self,
    ):
        self.corner_detector.detect_inferior_corner.return_value = (
            self.CORNER_TOO_MUCH_FORWARD
        )
        expected_movement_command = MovementCommand(
            Direction.FORWARD, Speed(ROBOT_ALIGNMENT_SPEED), CommandDuration(0)
        )

        actual_movement_command = (
            self.corner_alignment_corrector.calculate_vertical_correction(self.AN_IMAGE)
        )

        self.assertEqual(actual_movement_command, expected_movement_command)
