from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage


class StageHandlerSelector:
    def __init__(
        self,
        start_handler: IStageHandler,
        go_to_ohmmeter_handler: IStageHandler,
        read_command_panel_handler: IStageHandler,
        transport_puck: IStageHandler,
        stop_handler: IStageHandler,
    ):
        self._start_handler = start_handler
        self._go_to_ohmmeter_handler = go_to_ohmmeter_handler
        self._read_command_panel_handler = read_command_panel_handler
        self.transport_puck_handler = transport_puck
        self._stop_handler = stop_handler

    def select(self, stage: Stage) -> IStageHandler:
        if stage == Stage.START_CYCLE:
            return self._start_handler
        elif stage == Stage.GO_TO_OHMMETER:
            return self._go_to_ohmmeter_handler
        elif stage == Stage.READ_COMMAND_PANEL:
            return self._read_command_panel_handler
        elif stage == Stage.TRANSPORT_PUCK:
            return self.transport_puck_handler
        elif stage == Stage.STOP:
            return self._stop_handler
