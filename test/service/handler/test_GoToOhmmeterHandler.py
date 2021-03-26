import unittest
from unittest.mock import MagicMock

from domain.game.Stage import Stage
from domain.resistance.Resistance import Resistance
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler


class TestGoToOhmmeterHandler(unittest.TestCase):
    A_RESISTANCE = Resistance(123)
    SOME_MOVEMENTS = MagicMock()

    def setUp(self) -> None:
        self.communication_service = MagicMock()
        self.movement_service = MagicMock()
        self.resistance_service = MagicMock()
        self.go_to_ohmmeter_handler = GoToOhmmeterHandler(
            self.communication_service, self.movement_service, self.resistance_service
        )

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
