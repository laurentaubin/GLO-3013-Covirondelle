from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage


class StageHandlerSelector:
    def __init__(
        self,
        start_game_cycle_handler: IStageHandler,
        go_to_ohmmeter_handler: IStageHandler,
        find_command_panel_handler: IStageHandler,
        transport_puck_handler: IStageHandler,
        stop_handler: IStageHandler,
    ):
        self.handlers = {
            Stage.START_CYCLE: start_game_cycle_handler,
            Stage.GO_TO_OHMMETER: go_to_ohmmeter_handler,
            Stage.READ_COMMAND_PANEL: find_command_panel_handler,
            Stage.TRANSPORT_PUCK: transport_puck_handler,
            Stage.STOP: stop_handler,
        }

    def select(self, stage: Stage) -> IStageHandler:
        return self.handlers.get(stage)
