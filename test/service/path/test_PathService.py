from unittest import TestCase
from unittest.mock import MagicMock, patch

from domain.Position import Position
from domain.StartingZoneCorner import StartingZoneCorner
from service.path.PathService import PathService


class TestPathService(TestCase):
    A_CORNER_LETTER = StartingZoneCorner.A
    ANOTHER_CORNER_LETTER = StartingZoneCorner.B
    A_CORNER_POSITION = Position(12, 12)
    A_ROBOT_POSITION = Position(200, 200)
    A_GAME_TABLE = MagicMock()
    A_STARTING_ZONE = MagicMock()
    A_POSITION = MagicMock()

    def setUpMocks(self) -> None:
        self.game_table = MagicMock()
        self.shortest_path_algorithm = MagicMock()

        self.game_table.get_starting_zone.return_value = self.A_STARTING_ZONE

    def setUp(self) -> None:
        self.setUpMocks()

        self.path_service = PathService(
            self.shortest_path_algorithm,
        )
        self.path_service.set_game_table(self.A_GAME_TABLE)
        self.path_service.set_first_corner_letter(self.A_CORNER_LETTER)

    def test_givenRobotSendsLetterA_whenFindPathToNextStartingZoneCorner_thenFindPositionOfCornerA(
        self,
    ):
        self.A_GAME_TABLE.get_starting_zone.return_value = self.A_STARTING_ZONE

        self.path_service.find_path_to_next_starting_zone_corner(self.A_ROBOT_POSITION)

        self.A_STARTING_ZONE.find_corner_position_from_letter.assert_called_with(
            self.A_CORNER_LETTER
        )

    @patch.object(StartingZoneCorner, "get_next_corner")
    def test_givenTwoSuccessiveCalls_whenFindPathToNextStartingZoneCorner_thenCornerOrderIsFollowed(
        self, startingZoneCorner_mock
    ):
        self.A_GAME_TABLE.get_starting_zone.return_value = self.A_STARTING_ZONE
        startingZoneCorner_mock.return_value = self.ANOTHER_CORNER_LETTER

        self.path_service.find_path_to_next_starting_zone_corner(self.A_ROBOT_POSITION)
        self.path_service.find_path_to_next_starting_zone_corner(self.A_ROBOT_POSITION)

        self.A_STARTING_ZONE.find_corner_position_from_letter.assert_has_calls(
            self.A_STARTING_ZONE.find_corner_position_from_letter(self.A_CORNER_LETTER),
            self.A_STARTING_ZONE.find_corner_position_from_letter(
                self.ANOTHER_CORNER_LETTER
            ),
        )

    def test_whenFindPathToNextStartingZoneCorner_thenPathIsCalculatedWithRightCornerPositionAndRobotPosition(
        self,
    ):
        self.A_GAME_TABLE.get_starting_zone.return_value = self.A_STARTING_ZONE
        self.A_STARTING_ZONE.find_corner_position_from_letter.return_value = (
            self.A_CORNER_POSITION
        )

        self.path_service.find_path_to_next_starting_zone_corner(self.A_ROBOT_POSITION)

        self.shortest_path_algorithm.find_shortest_path.assert_called_with(
            self.A_ROBOT_POSITION, self.A_CORNER_POSITION
        )

    def test_givenGameTable_whenSetGameTable_thenShortestPathAlgorithmMazeIsSet(self):
        a_maze = MagicMock()
        self.A_GAME_TABLE.get_maze.return_value = a_maze

        self.path_service.set_game_table(self.A_GAME_TABLE)

        self.shortest_path_algorithm.set_maze.assert_called_with(a_maze)
