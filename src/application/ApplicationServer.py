from threading import Thread

from application.RobotStatusReceiver import RobotStatusReceiver
from application.VisionWorker import VisionWorker
from application.WebServer import WebServer
from domain.game.IGameCycle import IGameCycle


class ApplicationServer:
    def __init__(
        self,
        robot_status_receiver: RobotStatusReceiver,
        game_cycle: IGameCycle,
        vision_worker: VisionWorker,
        web_server: WebServer,
    ):
        self._robot_status_receiver_thread = Thread(
            target=robot_status_receiver.run, daemon=True
        )
        self._vision_worker_thread = Thread(target=vision_worker.run, daemon=True)
        self._web_server_thread = Thread(target=web_server.run, daemon=True)

        self.game_cycle = game_cycle

    def run(self):
        self._robot_status_receiver_thread.start()
        self._vision_worker_thread.start()
        self._web_server_thread.start()
        self.game_cycle.run()

    def stop(self):
        self._robot_status_receiver_thread.join()
        self._vision_worker_thread.join()
        self._web_server_thread.join()

        self.game_cycle.stop()
