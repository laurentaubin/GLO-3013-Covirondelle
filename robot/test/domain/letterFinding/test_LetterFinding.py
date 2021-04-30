from unittest import TestCase

from domain.letterFinding.CommandPanelTargetCellIndex import CommandPanelTargetCellIndex
from domain.exception.CommandPanelTargetException import CommandPanelTargetException
from domain.resistance.Resistance import Resistance
from infra.vision.CommandPanelPosition import CommandPanelPosition


class TestCommandPanelTargetCellIndex(TestCase):
    def setUp(self) -> None:

        self._command_panel_target_position = CommandPanelTargetCellIndex()

    def test_givenAResistanceWithCorrectValue_whenCallGetTargetCellIndex_ReturnTheRithCommandPanel(
        self,
    ):
        a_valid_resistance = Resistance(730)

        command_panel_position = (
            self._command_panel_target_position.get_target_cell_indix(
                a_valid_resistance
            )
        )

        self.assertEqual(command_panel_position, CommandPanelPosition.LOWER_LEFT)

    def test_givenAResistanceWithNotCorrectValue_whenCallGetTargetCellIndex_ReturnException(
        self,
    ):

        a_wrong_resistance = Resistance(0)

        with self.assertRaises(CommandPanelTargetException):
            self._command_panel_target_position.get_target_cell_indix(
                a_wrong_resistance
            )
