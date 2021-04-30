from threading import Thread

from domain.game.IGameCycle import IGameCycle


class ApplicationServer:
    def __init__(self, communication_runner, game_cycle: IGameCycle):
        self.communication_runner = communication_runner
        self.game_cycle = game_cycle

        self.communication_runner_thread = Thread(
            target=communication_runner.run, daemon=True
        )

    def run(self) -> None:
        self.communication_runner_thread.start()
        self.game_cycle.run()

    def stop(self) -> None:
        self.communication_runner_thread.join()
        self.game_cycle.stop()
