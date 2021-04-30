from domain.Color import Color
from domain.Position import Position


class Puck:
    def __init__(self, color: Color, position: Position):
        self._color = color
        self._position = position

    def get_color(self) -> Color:
        return self._color

    def get_position(self) -> Position:
        return self._position
