from domain.communication.Message import Message
from domain.game.IGameCycle import IGameCycle
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from service.communication.CommunicationService import CommunicationService
from service.game.StageService import StageService

STAGE_COMPLETED = True


class SlaveGameCycle(IGameCycle):
    def __init__(
        self, communicationService: CommunicationService, stage_service: StageService
    ):
        self.communication_service = communicationService
        self.stage_service = stage_service

    def run(self) -> None:
        self._confirm_boot()
        self._wait_until_start_signal()
        print("\n")
        self._go_to_ohmmeter()
        print("\n")
        self._find_command_panel()
        print("\n")
        self._transport_puck()
        print("\n")
        self._stop()

    def _wait_until_start_signal(self):
        self.stage_service.execute(Stage.START_CYCLE)

    def _go_to_ohmmeter(self):
        self.stage_service.execute(Stage.GO_TO_OHMMETER)

    def _find_command_panel(self):
        self.stage_service.execute(Stage.READ_COMMAND_PANEL)

    def _transport_puck(self):
        self.stage_service.execute(Stage.TRANSPORT_PUCK)

    def _stop(self):
        self.stage_service.execute(Stage.STOP)

    def _confirm_boot(self):
        message = Message(Topic.BOOT, None)
        self.communication_service.send_object(message)
