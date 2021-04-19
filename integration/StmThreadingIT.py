import time
from threading import Thread

from IntegrationContext import IntegrationContext


class StmThreadingIT(IntegrationContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)
        self.communication_runner_thread = Thread(
            target=self.communication_runner.run, daemon=True
        )

    def run(self):
        self.communication_runner_thread.start()
        self.send_a_bunch_of_rotation_commands()

    def send_a_bunch_of_rotation_commands(self):
        while True:
            self._movement_service.rotate(83)
            time.sleep(0.5)


if __name__ == "__main__":
    stm_threading_it = StmThreadingIT(False)
    stm_threading_it.run()
