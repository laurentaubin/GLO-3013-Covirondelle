from domain.game.Stage import Stage
from service.game.StageHandlerSelector import StageHandlerSelector


class StageService:
    def __init__(self, stage_handler_selector: StageHandlerSelector):
        self.stage_handler_selector = stage_handler_selector

    def execute(self, stage: Stage):
        self.stage_handler_selector.select(stage).execute()
