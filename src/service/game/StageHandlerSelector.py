from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage


class StageHandlerSelector:
    def __init__(
        self,
        go_to_ohmmeter_handler: IStageHandler,
        find_command_panel_handler: IStageHandler,
        transport_puck: IStageHandler,
        go_park_handler: IStageHandler,
        stop_handler: IStageHandler,
    ):
        self._go_to_ohmmeter_handler = go_to_ohmmeter_handler
        self._find_command_panel_handler = find_command_panel_handler
        self.transport_puck_handler = transport_puck
        self._go_park_handler = go_park_handler
        self._stop_handler = stop_handler

    def select(self, stage: Stage) -> IStageHandler:
        if stage == Stage.GO_TO_OHMMETER:
            return self._go_to_ohmmeter_handler
        elif stage == Stage.FIND_COMMAND_PANEL:
            return self._find_command_panel_handler
        elif stage == Stage.TRANSPORT_PUCK:
            return self.transport_puck_handler
        elif stage == Stage.GO_PARK:
            return self._go_park_handler
        elif stage == Stage.STOP:
            return self._stop_handler
