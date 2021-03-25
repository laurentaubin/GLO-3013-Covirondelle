from domain.game.IGameCycle import IGameCycle
from domain.game.Stage import Stage
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
        self._wait_until_start_signal()
        print("\n")
        self._go_to_ohmmeter()
        print("\n")
        self._find_command_panel()
        print("\n")
        self._transport_puck()
        print("\n")
        self._go_park()
        print("\n")
        self._stop()

    def _wait_until_start_signal(self):
        while True:
            print("Waiting for start signal ...")
            message = self.communication_service.receive_game_cycle_message()
            print("Message received in game cycle: " + message)
            if message == Stage.START_CYCLE.value:
                self.communication_service.send_game_cycle_message(
                    Stage.STAGE_COMPLETED.value
                )
                break

    def _go_to_ohmmeter(self):
        while True:
            print("Waiting for go_to_ohmmeter start signal")
            message = self.communication_service.receive_game_cycle_message()
            if message == Stage.GO_TO_OHMMETER.value:
                print("Starting go_to_ohmmeter stage")
                try:
                    self.stage_service.execute(Stage.GO_TO_OHMMETER)
                    break
                except RuntimeError:
                    pass

    def _find_command_panel(self):
        while True:
            print("Waiting for find_command_panel start signal")
            message = self.communication_service.receive_game_cycle_message()
            if message == Stage.FIND_COMMAND_PANEL.value:
                print("Starting find_command_panel stage")
                try:
                    self.stage_service.execute(Stage.FIND_COMMAND_PANEL)
                    self.communication_service.send_game_cycle_message(
                        Stage.STAGE_COMPLETED.value
                    )
                    break
                except RuntimeError:
                    pass

    def _transport_puck(self):
        while True:
            print("Waiting for transport_puck start signal")
            message = self.communication_service.receive_game_cycle_message()
            if message == Stage.TRANSPORT_PUCK.value:
                try:
                    print("Starting transport_puck stage")
                    self.stage_service.execute(Stage.TRANSPORT_PUCK)
                    self.communication_service.send_game_cycle_message(
                        Stage.STAGE_COMPLETED.value
                    )
                    break
                except RuntimeError:
                    pass

    def _go_park(self):
        while True:
            print("Waiting for go_park start signal")
            message = self.communication_service.receive_game_cycle_message()
            if message == Stage.GO_PARK.value:
                try:
                    print("Starting go_park stage")
                    self.stage_service.execute(Stage.GO_PARK)
                    self.communication_service.send_game_cycle_message(
                        Stage.STAGE_COMPLETED.value
                    )
                    break
                except RuntimeError:
                    pass

    def _stop(self):
        while True:
            print("Waiting for stop signal")
            message = self.communication_service.receive_game_cycle_message()
            if message == Stage.STOP.value:
                try:
                    print("Starting stop sequence")
                    self.stage_service.execute(Stage.STOP)
                    self.communication_service.send_game_cycle_message(
                        Stage.STAGE_COMPLETED.value
                    )
                    break
                except RuntimeError:
                    pass
