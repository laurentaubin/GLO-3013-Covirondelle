import unittest
from unittest.mock import MagicMock, patch

from config.config import MIN_VERTICAL_ANGLE_VALUE
from domain.game.Stage import Stage
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.resistance.Resistance import Resistance
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler


@patch("time.sleep", MagicMock())
class TestGoToOhmmeterHandler(unittest.TestCase):
    A_RESISTANCE = Resistance(123)
    SOME_MOVEMENTS = MagicMock()
    A_STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CommandDuration(0)
    )
    A_MOVEMENT_COMMAND = MagicMock()
    A_SLOW_MOVEMENT_COMMAND = MagicMock()
    AN_IMAGE = MagicMock()

    def setUp(self) -> None:
        self.communication_service = MagicMock()
        self.movement_service = MagicMock()
        self.resistance_service = MagicMock()
        self.vision_service = MagicMock()
        self.ohmmeter_alignment_corrector = MagicMock()
        self.movement_command_factory = MagicMock()
        self.go_to_ohmmeter_handler = GoToOhmmeterHandler(
            self.communication_service,
            self.movement_service,
            self.resistance_service,
            self.vision_service,
            self.ohmmeter_alignment_corrector,
            self.movement_command_factory,
        )
        self._setup_no_alignment_correction_needed()

    def test_whenExecute_thenSendGameCycleMessageIsCalledTwice(self):
        self.communication_service.receive_game_cycle_message.return_value = (
            Stage.GO_TO_OHMMETER.value
        )
        self.go_to_ohmmeter_handler.execute()

        call_count = self.communication_service.send_game_cycle_message.call_count

        self.assertEqual(2, call_count)

    def test_givenMovementsByStation_whenExecute_thenMovementServiceIsCalledWithMovements(
        self,
    ):
        self.communication_service.receive_object.return_value = self.SOME_MOVEMENTS

        self.go_to_ohmmeter_handler.execute()

        self.movement_service.move.assert_called_with(self.SOME_MOVEMENTS)

    def test_whenExecute_thenMakeCameraLookDown(self):
        self.go_to_ohmmeter_handler.execute()

        self.vision_service.rotate_camera_vertically.assert_called_with(
            MIN_VERTICAL_ANGLE_VALUE
        )

    def test_whenExecute_thenCameraTakeImage(self):
        self.go_to_ohmmeter_handler.execute()

        self.vision_service.take_image.assert_called()

    def test_givenACurrentImage_whenExecute_thenHorizontalAlignmentIsCalculatedFromImage(
        self,
    ):
        self.vision_service.take_image.return_value = self.AN_IMAGE

        self.go_to_ohmmeter_handler.execute()

        self.ohmmeter_alignment_corrector.calculate_horizontal_correction.assert_called_with(
            self.AN_IMAGE
        )

    def test_givenNotHorizontallyAligned_whenExecute_thenHorizontalCorrectionIsCalculatedUntilAligned(
        self,
    ):
        self._setup_horizontal_correction_needed()
        number_of_horizontal_correction_calculation_needed = 2

        self.go_to_ohmmeter_handler.execute()

        self.assertEqual(
            number_of_horizontal_correction_calculation_needed,
            self.ohmmeter_alignment_corrector.calculate_horizontal_correction.call_count,
        )

    def test_givenNotHorizontallyAligned_whenExecute_thenHorizontalAlignmentMovementCommandAreExecuted(
        self,
    ):
        self._setup_horizontal_correction_needed()
        sum_of_horizontal_movement_command_needed = 4

        self.go_to_ohmmeter_handler.execute()

        self.assertEqual(
            sum_of_horizontal_movement_command_needed,
            self.movement_service.execute_movement_command.call_count,
        )

    def test_whenExecute_thenASlowBackwardMovementCommandIsCreated(self):
        self.go_to_ohmmeter_handler.execute()

        self.movement_command_factory.create_alignment_movement_command.assert_called()

    def test_whenExecute_thenMoveSlowlyBackwards(self):
        self.movement_command_factory.create_slow_continuous_backwards_movement_command.return_value = (
            self.A_SLOW_MOVEMENT_COMMAND
        )

        self.go_to_ohmmeter_handler.execute()

        self.movement_service.execute_movement_command.called_with(
            self.A_SLOW_MOVEMENT_COMMAND
        )

    def test_givenNotInContactWithOhmmeter_whenExecute_thenMoveBackwardUntilInContact(
        self,
    ):
        self._setup_not_in_contact_with_ohmmeter()
        number_of_times_confirm_contact_needed = 2

        self.go_to_ohmmeter_handler.execute()

        self.assertEqual(
            number_of_times_confirm_contact_needed,
            self.resistance_service.confirm_contact.call_count,
        )

    def test_whenExecute_thenResistanceServiceIsCalled(self):
        self.go_to_ohmmeter_handler.execute()

        self.resistance_service.take_resistance_measurement.assert_called()

    def test_givenResistanceValueByResistanceService_whenExecute_thenResistanceObjectIsSentToStation(
        self,
    ):
        self.resistance_service.take_resistance_measurement.return_value = (
            self.A_RESISTANCE
        )

        self.go_to_ohmmeter_handler.execute()

        self.communication_service.send_object.assert_called_with(self.A_RESISTANCE)

    def _setup_no_alignment_correction_needed(self):
        self.ohmmeter_alignment_corrector.calculate_horizontal_correction.return_value = (
            self.A_STOP_MOVEMENT_COMMAND
        )
        self.resistance_service.make_contact.return_value = True

    def _setup_horizontal_correction_needed(self):
        self.ohmmeter_alignment_corrector.calculate_horizontal_correction.side_effect = [
            self.A_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
        ]
        self.resistance_service.make_contact.return_value = True

    def _setup_not_in_contact_with_ohmmeter(self):
        self.resistance_service.confirm_contact.side_effect = [False, True]
