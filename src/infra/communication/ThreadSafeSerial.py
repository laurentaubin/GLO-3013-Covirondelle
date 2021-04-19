import threading

from serial import Serial


class ThreadSafeSerial(Serial):
    def __init__(self, port_name: str, baud_rate: int):
        super().__init__(port=port_name, baudrate=baud_rate)
        self._lock = threading.Lock()

    def write(self, data: str):
        with self._lock:
            super().write(data)

    def write_and_readline(self, data: str):
        with self._lock:
            super().write(data)
            return super().readline()
