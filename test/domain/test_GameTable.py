from unittest import TestCase
from unittest.mock import MagicMock

from domain.Color import Color
from domain.GameTable import GameTable
from domain.Position import Position
from domain.Puck import Puck


class TestGameTable(TestCase):
    A_STARTING_ZONE = MagicMock()
    A_MAZE = MagicMock()
    A_PUCK_ZONE_CENTER = Position(100, 100)
    A_PUCK_LIST = [
        Puck(color, Position(200, 200)) for color in Color if color != Color.NONE
    ]

    def setUp(self) -> None:
        self.game_table = GameTable(
            self.A_STARTING_ZONE, self.A_MAZE, self.A_PUCK_ZONE_CENTER, self.A_PUCK_LIST
        )

    def test_givenRedColor_whenGetPuck_thenReturnRedPuck(self):
        red_color = Color.RED
        actual_puck = self.game_table.get_puck(red_color)

        self.assertEqual(actual_puck.get_color(), red_color)

    def test_givenGreenColor_whenGetPuck_thenReturnGreenPuck(self):
        green_color = Color.GREEN
        actual_puck = self.game_table.get_puck(green_color)

        self.assertEqual(actual_puck.get_color(), green_color)
