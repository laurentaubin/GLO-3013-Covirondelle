from context.StationContext import StationContext


class IntegrationContext(StationContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)
        game_table = self._vision_service.create_game_table()
        self._path_service.set_game_table(game_table)
