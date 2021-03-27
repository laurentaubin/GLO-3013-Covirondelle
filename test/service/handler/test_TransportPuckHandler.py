from typing import List
from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.game.Stage import Stage
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.Speed import Speed
from domain.vision.Color import Color
from service.handler.TransportPuckHandler import TransportPuckHandler


class TestTransportPuckHandler(TestCase):
    ONE_PUCK_TO_TRANSPORT: List[Color] = [Color.RED]
    MANY_PUCKS_TO_TRANSPORT: List[Color] = [Color.RED, Color.GREEN, Color.BLUE]
    AN_IMAGE = MagicMock()
    A_MOVEMENT_COMMAND = MagicMock()
    A_STOP_MOVEMENT_COMMAND = MovementCommand(
        Direction.STOP, Speed(0), CommandDuration(0)
    )

    def setUp(self) -> None:
        self.communication_service = MagicMock()
        self.vision_service = MagicMock()
        self.movement_service = MagicMock()
        self.puck_alignment_corrector = MagicMock()

        self.transport_puck_handler = TransportPuckHandler(
            self.communication_service,
            self.vision_service,
            self.movement_service,
            self.puck_alignment_corrector,
        )

    def test_whenExecute_thenStageStartedIsSentToStation(self):
        self.transport_puck_handler.execute()

        self.communication_service.send_game_cycle_message.assert_called_with(
            Stage.STAGE_STARTED
        )

    def test_whenExecute_thenPucksToTransportAreReceived(self):
        self.transport_puck_handler.execute()

        self.communication_service.receive_object.assert_called()

    @patch("time.sleep", return_value=None)
    def test_whenExecute_thenImageIsTaken(self, patched_time_sleep):
        self._setup_receive_one_puck_to_transport()

        self.transport_puck_handler.execute()

        self.vision_service.take_image.assert_called()

    @patch("time.sleep", return_value=None)
    def test_whenExecute_thenPuckToTransportAndImageFromVisionServiceAreUsedToHorizontallyAlignRobotWithPuck(
        self, patched_time_sleep
    ):
        self._setup_receive_one_puck_to_transport()

        self.transport_puck_handler.execute()

        self.puck_alignment_corrector.calculate_horizontal_correction.assert_called_with(
            self.AN_IMAGE, self.ONE_PUCK_TO_TRANSPORT[0]
        )

    @patch("time.sleep", return_value=None)
    def test_givenOnePuckToTransport_whenExecute_thenPuckToTransportAndImageFromVisionServiceAreUsedToVerticallyAlignRobotWithPuck(
        self, patched_time_sleep
    ):
        self._setup_receive_one_puck_to_transport()

        self.transport_puck_handler.execute()

        self.puck_alignment_corrector.calculate_vertical_correction.assert_called_with(
            self.AN_IMAGE, self.ONE_PUCK_TO_TRANSPORT[0]
        )

    @patch("time.sleep", return_value=None)
    def test_givenManyPucks_whenExecute_thenHorizontalCorrectionIsCalculatedForEachPuck(
        self, patched_time_sleep
    ):
        self._setup_corrections_for_many_pucks()

        self.transport_puck_handler.execute()

        self.assertEqual(
            len(self.MANY_PUCKS_TO_TRANSPORT),
            self.puck_alignment_corrector.calculate_horizontal_correction.call_count,
        )

    @patch("time.sleep", return_value=None)
    def test_givenManyPucks_whenExecute_thenVerticalCorrectionIsCalculatedForEachPuck(
        self, patch_time_sleep
    ):
        self._setup_corrections_for_many_pucks()

        self.transport_puck_handler.execute()

        self.assertEqual(
            len(self.MANY_PUCKS_TO_TRANSPORT),
            self.puck_alignment_corrector.calculate_vertical_correction.call_count,
        )

    @patch("time.sleep", return_value=None)
    def test_givenManyPucksToTransportAllCorrectlyAligned_whenExecute_thenAlignRobotWithEachPuck(
        self, patched_time_sleep
    ):
        self._setup_corrections_for_many_pucks()
        no_movement_command_executed = 0

        self.transport_puck_handler.execute()

        self.assertEqual(
            no_movement_command_executed,
            self.movement_service.execute_movement_command.call_count,
        )

    @patch("time.sleep", return_value=None)
    def test_givenAPuckNotVerticallyAndHorizontallyAlign_whenExecute_thenShouldCorrectHorizontalAndVerticalAlignment(
        self, patch_time_sleep
    ):
        self._setup_receive_one_puck_not_correctly_aligned()
        sum_of_horizontal_and_vertical_correction_movement_needed = 4

        self.transport_puck_handler.execute()

        self.assertEqual(
            sum_of_horizontal_and_vertical_correction_movement_needed,
            self.movement_service.execute_movement_command.call_count,
        )

    def _setup_receive_one_puck_to_transport(self):
        self.communication_service.receive_object.return_value = (
            self.ONE_PUCK_TO_TRANSPORT
        )
        self.puck_alignment_corrector.calculate_horizontal_correction.side_effect = [
            self.A_STOP_MOVEMENT_COMMAND
        ]
        self.puck_alignment_corrector.calculate_vertical_correction.side_effect = [
            self.A_STOP_MOVEMENT_COMMAND
        ]
        self.vision_service.take_image.return_value = self.AN_IMAGE

    def _setup_receive_one_puck_not_correctly_aligned(self):
        self.communication_service.receive_object.return_value = (
            self.ONE_PUCK_TO_TRANSPORT
        )
        self.puck_alignment_corrector.calculate_horizontal_correction.side_effect = [
            self.A_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
        ]
        self.puck_alignment_corrector.calculate_vertical_correction.side_effect = [
            self.A_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
        ]
        self.vision_service.take_image.return_value = self.AN_IMAGE

    def _setup_corrections_for_many_pucks(self):
        self.communication_service.receive_object.return_value = (
            self.MANY_PUCKS_TO_TRANSPORT
        )
        self.puck_alignment_corrector.calculate_horizontal_correction.side_effect = [
            self.A_STOP_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
        ]
        self.puck_alignment_corrector.calculate_vertical_correction.side_effect = [
            self.A_STOP_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
            self.A_STOP_MOVEMENT_COMMAND,
        ]
