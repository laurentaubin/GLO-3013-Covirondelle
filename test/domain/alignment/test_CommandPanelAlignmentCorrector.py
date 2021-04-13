from unittest import TestCase
from unittest.mock import MagicMock

from config.config import ROBOT_ALIGNMENT_SPEED
from domain.Position import Position
from domain.alignment.CommandPanelAlignmentCorrector import (
    CommandPanelAlignmentCorrector,
)
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed


class TestCommandPanelAlignmentCorrector(TestCase):
    AN_IMAGE = MagicMock()
    ALIGNMENT_SPEED = Speed(ROBOT_ALIGNMENT_SPEED)
    NUMBER_OF_COMMAND_PANEL_LETTERS = 9
    COMMAND_PANEL_REFERENCE_POSITION = Position(20, 20)
    ANY_POSITION = Position(178, 248)
    A_POSITION_HORIZONTALLY_ALIGNED = Position(20, 20)
    A_LEFT_POSITION = Position(10, 42)
    A_RIGHT_POSITION = Position(200, 211)
    A_LEFT_POSITION_WITHIN_THRESHOLD = Position(345, 332)
    A_RIGHT_POSITION_WITHIN_THRESHOLD = Position(355, 332)
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CONTINUOUS_COMMAND_DURATION
    )
    NINE_LETTERS_READ = ["A", "A", "A", "A", "A", "A", "A", "A", "A"]

    def setUp(self) -> None:
        self.panel_detector = MagicMock()
        self.command_panel_letter_extractor = MagicMock()

        self.command_panel_alignment_corrector = CommandPanelAlignmentCorrector(
            self.NUMBER_OF_COMMAND_PANEL_LETTERS,
            self.COMMAND_PANEL_REFERENCE_POSITION,
            self.panel_detector,
            self.command_panel_letter_extractor,
        )

    def test_givenCanReadAllLettersOnCommandPanel_whenCalculateHorizontalAlignment_thenReturnStopMovementCommand(
        self,
    ):
        self.command_panel_letter_extractor.extract_letters_from_image.return_value = (
            self.NINE_LETTERS_READ
        )

        actual_command_movement = (
            self.command_panel_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, self.STOP_MOVEMENT_COMMAND)

    def test_givenRobotTooMuchToTheLeft_whenCalculateHorizontalAlignment_thenReturnRightMovementCommand(
        self,
    ):
        self.panel_detector.detect_upper_left_corner.return_value = (
            self.A_RIGHT_POSITION
        )

        expected_movement_command = MovementCommand(
            Direction.RIGHT, self.ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
        )

        actual_command_movement = (
            self.command_panel_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, expected_movement_command)

    def test_givenRobotTooMuchOnTheRight_whenCalculateHorizontalAlignment_thenReturnLeftMovementCommand(
        self,
    ):
        self.panel_detector.detect_upper_left_corner.return_value = self.A_LEFT_POSITION

        expected_movement_command = MovementCommand(
            Direction.LEFT, self.ALIGNMENT_SPEED, self.CONTINUOUS_COMMAND_DURATION
        )

        actual_command_movement = (
            self.command_panel_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_command_movement, expected_movement_command)
