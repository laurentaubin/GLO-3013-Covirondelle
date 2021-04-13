from domain.communication.ILed import ILed
from domain.communication.StmCommand import StmCommand
from serial import Serial


class StmLed(ILed):
    def __init__(self, serial: Serial):
        self._serial = serial
        self._is_led_on = False

    def get_led_status(self):
        return self._is_led_on

    def toggle_led(self):
        command = bytes([StmCommand.TOGGLE_LED])
        self._serial.write(command)
        self._is_led_on = not self._is_led_on
