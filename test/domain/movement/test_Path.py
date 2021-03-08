from unittest import TestCase

from domain.exception.PositionNotAdjacentException import PositionNotAdjacentException
from domain.movement.Path import Path
from domain.movement.Position import Position


class TestPath(TestCase):
    def test_givenEmptyPath_whenGetItem_thenIndexErrorIsRaised(self):
        path = Path([])

        with self.assertRaises(IndexError):
            _ = path[0]

    def test_givenPathWithTwoPositions_whenGetSecondItem_thenSecondPositionIsReturned(
        self,
    ):
        first_position = Position(1, 1)
        second_position = Position(1, 2)
        path = Path([first_position, second_position])

        actual_position = path[1]

        self.assertEqual(second_position, actual_position)

    def test_givenPathWithTwoPositions_whenGettingLengthOfPath_thenReturnTwo(self):

        first_position = Position(1, 1)
        second_position = Position(1, 2)
        path = Path([first_position, second_position])

        path_length = len(path)

        self.assertEqual(2, path_length)

    def test_givenEmptyPath_whenAdd_thenPositionIsAddedToPath(self):
        path = Path([])
        a_position = Position(1, 1)

        path.add(a_position)

        self.assertEqual(a_position, path[0])

    def test_givenPathWithPosition_whenAddAdjacentPosition_thenPositionIsAddedToPath(
        self,
    ):
        path = Path([Position(1, 2)])
        a_position = Position(1, 1)

        path.add(a_position)

        self.assertEqual(a_position, path[1])

    def test_givenPathWithPosition_whenAddHorizontallyNonAdjacentPosition_thenThrowInvalidPositionException(
        self,
    ):
        path = Path([Position(3, 1)])
        a_position = Position(1, 1)

        with self.assertRaises(PositionNotAdjacentException):
            path.add(a_position)

    def test_givenPathWithPosition_whenAddVerticallyNonAdjacentPosition_thenThrowInvalidPositionException(
        self,
    ):
        path = Path([Position(1, 3)])
        a_position = Position(1, 1)

        with self.assertRaises(PositionNotAdjacentException):
            path.add(a_position)
