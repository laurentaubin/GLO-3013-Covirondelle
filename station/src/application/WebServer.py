from flask import Flask, jsonify

from application.GameStateDtoAssembler import GameStateDtoAssembler
from domain.game.GameState import GameState


class WebServer:
    def __init__(self, game_state_dto_assembler: GameStateDtoAssembler):
        self.app = Flask(__name__)
        self.app.add_url_rule("/information", "information", self.get_robot_status)
        self.app.add_url_rule(
            "/start", "start", self.start_game_cycle, methods=["POST"]
        )
        self._game_state_dto_assembler = game_state_dto_assembler

    def run(self):
        self.app.run()

    def get_robot_status(self):
        game_state_dto = self._game_state_dto_assembler.assemble_from_game_state(
            GameState.get_instance()
        )
        return jsonify(game_state_dto.__dict__)

    def start_game_cycle(self):
        GameState.get_instance().start_game_cycle()
        return {"is_game_started": True}
