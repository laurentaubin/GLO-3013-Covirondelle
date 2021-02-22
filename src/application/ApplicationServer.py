from threading import Thread

from application.RobotStatusReceiver import RobotStatusReceiver
from domain.game.IGameCycle import IGameCycle


class ApplicationServer:
    def __init__(
        self, robot_status_receiver: RobotStatusReceiver, game_cycle: IGameCycle
    ):
        self.robot_status_receiver = robot_status_receiver
        self.robot_status_receiver_thread = Thread(
            target=self.robot_status_receiver.run, daemon=True
        )

        self.game_cycle = game_cycle

    def run(self):
        self.robot_status_receiver_thread.start()

        self.game_cycle.run()

    def stop(self):
        self.robot_status_receiver_thread.join()

        self.game_cycle.stop()
