from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.Position import Position
from domain.alignment.CommandPanelAlignmentCorrector import (
    CommandPanelAlignmentCorrector,
)
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement


@patch("time.sleep", MagicMock(return_value=0))
class TestCommandPanelAlignmentCorrector(TestCase):
    AN_IMAGE = MagicMock()
    ALIGNMENT_DISTANCE = Distance(0.1)
    NUMBER_OF_COMMAND_PANEL_LETTERS = 9
    COMMAND_PANEL_REFERENCE_POSITION = Position(20, 20)
    ANY_POSITION = Position(178, 248)
    A_POSITION_HORIZONTALLY_ALIGNED = Position(20, 20)
    A_LEFT_POSITION = Position(10, 42)
    A_RIGHT_POSITION = Position(200, 211)
    A_LEFT_POSITION_WITHIN_THRESHOLD = Position(345, 332)
    A_RIGHT_POSITION_WITHIN_THRESHOLD = Position(355, 332)
    CONTINUOUS_COMMAND_DURATION = CommandDuration(0)
    STOP_MOVEMENT = Movement(Direction.STOP, Distance(0))
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

    def test_givenCanReadAllLettersOnCommandPanel_whenCalculateHorizontalAlignment_thenReturnStopMovement(
        self,
    ):
        self.command_panel_letter_extractor.extract_letters_from_image.return_value = (
            self.NINE_LETTERS_READ
        )

        actual_movement = (
            self.command_panel_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement, self.STOP_MOVEMENT)

    def test_givenCommandPanelTooMuchOnTheRight_whenCalculateHorizontalAlignment_thenReturnRightMovement(
        self,
    ):
        self.panel_detector.detect_upper_left_corner.return_value = (
            self.A_RIGHT_POSITION
        )

        expected_movement = Movement(Direction.RIGHT, self.ALIGNMENT_DISTANCE)

        actual_movement = (
            self.command_panel_alignment_corrector.calculate_horizontal_correction(
                self.AN_IMAGE
            )
        )

        self.assertEqual(actual_movement, expected_movement)
