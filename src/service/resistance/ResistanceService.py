from domain.resistance.IOhmmeter import IOhmmeter
from domain.resistance.Resistance import Resistance


class ResistanceService:
    def __init__(self, resistance_threshold: float, ohmmeter: IOhmmeter):
        self._resistance_threshold = resistance_threshold
        self._ohmmeter = ohmmeter

    def confirm_contact(self) -> bool:
        resistance_read = abs(self._ohmmeter.read_resistance())

        print(resistance_read)
        return resistance_read <= self._resistance_threshold

    def take_resistance_measurement(self) -> Resistance:
        resistance_read = self._ohmmeter.read_resistance()
        print()
        print()
        print(resistance_read)
        print()
        print()
        return Resistance.round_to_nearest_e12_value(resistance_read)
