from unittest import TestCase
from unittest.mock import MagicMock

from domain.Position import Position
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.resistance.ResistanceColor import ResistanceColor
from infra.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector


class TestPuckAlignmentCorrector(TestCase):
    A_PUCK_COLOR = ResistanceColor.BLUE
    AN_IMAGE = MagicMock()
    IMAGE_CENTRAL_POINT: Position = Position(500, 500)
    ANY_POSITION = Position(69, 420)
    POSITION_WITHIN_HORIZONTAL_THRESHOLD = Position(515, 500)
    POSITION_WITHIN_VERTICAL_THRESHOLD = Position(3211, 496)
    POSITION_TOO_FAR_TO_THE_RIGHT = Position(600, 500)
    POSITION_TOO_FAR_TO_THE_LEFT = Position(300, 500)
    POSITION_TOO_FAR_FORWARD = Position(324, 24)
    POSITION_TOO_CLOSE = Position(65, 843)
    CENTER_POSITION_THRESHOLD: int = 20

    def setUp(self) -> None:
        self.puck_detector = MagicMock()
        self.alignment_corrector = PuckAlignmentCorrector(
            self.IMAGE_CENTRAL_POINT, self.CENTER_POSITION_THRESHOLD, self.puck_detector
        )

    def test_givenAnImage_whenCalculateHorizontalCorrection_thenPuckPositionIsDetected(
        self,
    ):
        self.puck_detector.detect.return_value = self.ANY_POSITION

        self.alignment_corrector.calculate_horizontal_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.puck_detector.detect.assert_called_with(self.AN_IMAGE, self.A_PUCK_COLOR)

    def test_givenAnImageWithPuckOnTheRight_whenCalculateHorizontalCorrection_thenReturnMovementToBeHorizontallyAlign(
        self,
    ):
        self.puck_detector.detect.return_value = self.POSITION_TOO_FAR_TO_THE_RIGHT
        expected_movement = Movement(Direction.RIGHT, Distance(100))

        actual_movement = self.alignment_corrector.calculate_horizontal_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.assertEqual(actual_movement, expected_movement)

    def test_givenAnImageWithPuckOnTheLeft_whenCalculateHorizontalCorrection_thenLeftMovementToBeHorizontallyAlign(
        self,
    ):
        self.puck_detector.detect.return_value = self.POSITION_TOO_FAR_TO_THE_LEFT
        expected_movement = Movement(Direction.LEFT, Distance(200))

        actual_movement = self.alignment_corrector.calculate_horizontal_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        print(actual_movement.get_direction())

        self.assertEqual(actual_movement, expected_movement)

    def test_givenAnImageWithPuckWithinHorizontalThreshold_whenCalculateHorizontalCorrection_thenReturnStopMovement(
        self,
    ):
        self.puck_detector.detect.return_value = (
            self.POSITION_WITHIN_HORIZONTAL_THRESHOLD
        )
        expected_movement = Movement(Direction.STOP, Distance(0))

        actual_movement = self.alignment_corrector.calculate_horizontal_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.assertEqual(actual_movement, expected_movement)

    def test_givenAnImageWithPuckTooFarForward_whenCalculateVerticalCorrection_thenMoveForwardToGetCloser(
        self,
    ):
        self.puck_detector.detect.return_value = self.POSITION_TOO_FAR_FORWARD
        expected_movement = Movement(Direction.FORWARD, Distance(476))

        actual_movement = self.alignment_corrector.calculate_vertical_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.assertEqual(actual_movement, expected_movement)

    def test_givenAnImageWithPuckTooClose_whenCalculateVerticalCorrection_thenMoveBackwardsToGetFurther(
        self,
    ):
        self.puck_detector.detect.return_value = self.POSITION_TOO_CLOSE
        expected_movement = Movement(Direction.BACKWARDS, Distance(343))

        actual_movement = self.alignment_corrector.calculate_vertical_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.assertEqual(actual_movement, expected_movement)

    def test_givenAnImageWithPuckWithinVerticalThreshold_whenCalculateVerticalCorrection_thenStopMovement(
        self,
    ):
        self.puck_detector.detect.return_value = self.POSITION_WITHIN_VERTICAL_THRESHOLD
        expected_movement = Movement(Direction.STOP, Distance(0))

        actual_movement = self.alignment_corrector.calculate_vertical_correction(
            self.AN_IMAGE, self.A_PUCK_COLOR
        )

        self.assertEqual(actual_movement, expected_movement)
