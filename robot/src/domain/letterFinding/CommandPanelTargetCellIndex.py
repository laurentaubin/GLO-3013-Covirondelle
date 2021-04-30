from domain.resistance.Resistance import Resistance
from infra.vision.CommandPanelPosition import CommandPanelPosition
from domain.exception.CommandPanelTargetException import CommandPanelTargetException


class CommandPanelTargetCellIndex:
    def get_target_cell_indix(self, resistance: Resistance):
        position = resistance.find_nth_digit(0)
        try:
            return CommandPanelPosition(position - 1)
        except Exception:
            raise CommandPanelTargetException()
