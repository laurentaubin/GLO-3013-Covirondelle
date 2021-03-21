from unittest import TestCase

from domain.game.GameState import GameState


class TestGameState(TestCase):
    def test_whenInstantiate_thenInstancesAreEqual(self):
        first_game_state = GameState.get_instance()
        second_game_state = GameState.get_instance()

        self.assertEqual(first_game_state, second_game_state)
