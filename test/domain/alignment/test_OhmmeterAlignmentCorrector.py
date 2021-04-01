from unittest import TestCase
from unittest.mock import MagicMock

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.alignment.OhmmeterAlignmentCorrector import OhmmeterAlignmentCorrector
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed


class TestOhmmeterAlignmentCorrector(TestCase):
    AN_IMAGE = MagicMock()
    ALIGNMENT_SPEED = ROBOT_ALIGNMENT_SPEED
    HORIZONTAL_THRESHOLD = 10
    ALIGNED_OHMMETER_POSITION = Position(350, 200)
    ANY_POSITION = Position(69, 420)
    A_POSITION_HORIZONTALLY_ALIGNED = Position(345, 2)
    A_POSITION_TOO_FAR_TO_THE_LEFT = Position(300, 42)
    A_POSITION_TOO_FAR_TO_THE_RIGHT = Position(400, 211)
    A_LEFT_POSITION_WITHIN_THRESHOLD = Position(345, 332)
    A_RIGHT_POSITION_WITHIN_THRESHOLD = Position(355, 332)
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CONTINUOUS_COMMAND_DURATION
    )

    def setUp(self) -> None:
        self.starting_zone_line_detector = MagicMock()

        self.ohmmeter_alignment_corrector = OhmmeterAlignmentCorrector(
            self.ALIGNED_OHMMETER_POSITION,
            self.HORIZONTAL_THRESHOLD,
            self.starting_zone_line_detector,
        )

    def test_givenAnImage_whenCalculateHorizontalAlignment_thenStartingZoneLineIsDetected(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = self.ANY_POSITION

        self.ohmmeter_alignment_corrector.calculate_horizontal_correction(self.AN_IMAGE)

        self.starting_zone_line_detector.detect.assert_called_with(self.AN_IMAGE)

    def test_givenAnImagePerfectlyAligned_whenCalculateHorizontalAlignment_thenReturnStopMovementCommand(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = (
            self.A_POSITION_HORIZONTALLY_ALIGNED
        )

        actual_command_movement = (
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, self.STOP_MOVEMENT_COMMAND)

    def test_givenLineTooMuchToTheLeft_whenCalculateHorizontalAlignment_thenReturnLeftMovementCommand(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = (
            self.A_POSITION_TOO_FAR_TO_THE_LEFT
        )
        expected_movement_command = MovementCommand(
            Direction.LEFT, self.ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
        )

        actual_command_movement = (
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, expected_movement_command)

    def test_givenLineTooMuchOnTheRight_whenCalculateHorizontalAlignment_thenReturnRightMovementCommand(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = (
            self.A_POSITION_TOO_FAR_TO_THE_RIGHT
        )
        expected_movement_command = MovementCommand(
            Direction.RIGHT, self.ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
        )

        actual_command_movement = (
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, expected_movement_command)

    def test_givenLineToTheLeftWithinThreshold_whenCalculateHorizontalAlignment_thenReturnStopMovementCommand(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = (
            self.A_LEFT_POSITION_WITHIN_THRESHOLD
        )

        actual_movement_command = (
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement_command, self.STOP_MOVEMENT_COMMAND)

    def test_givenLineToTheRightWithinThreshold_whenCalculateHorizontalAlignment_thenReturnStopMovementCommand(
        self,
    ):
        self.starting_zone_line_detector.detect.return_value = (
            self.A_RIGHT_POSITION_WITHIN_THRESHOLD
        )

        actual_movement_command = (
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement_command, self.STOP_MOVEMENT_COMMAND)
