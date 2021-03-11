from unittest import TestCase

from domain.game.GameState import GameState


class TestGameState(TestCase):
    def test_whenInstantiate_thenInstancesAreEqual(self):
        first_game_state = GameState()
        second_game_state = GameState()

        self.assertEqual(first_game_state, second_game_state)
