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

    def setUpMocks(self) -> None:
        self.vision_service = MagicMock()
        self.communication_service = MagicMock()
        self.shortest_path_algorithm = MagicMock()
        self.a_starting_zone = MagicMock()
        self.a_position = MagicMock()

    def setUp(self) -> None:
        self.setUpMocks()

    def test_whenInitializingPathService_thenStartingZoneIsDetected(self):
        PathService(
            self.vision_service,
            self.communication_service,
            self.shortest_path_algorithm,
        )

        self.vision_service.find_starting_zone.assert_called()

    def test_givenRobotSendsLetterA_whenFindPathToNextStartingZoneCorner_thenFindPositionOfCornerA(
        self,
    ):
        self.vision_service.find_starting_zone.return_value = self.a_starting_zone
        self.communication_service.get_first_corner_letter.return_value = (
            self.A_CORNER_LETTER
        )
        path_service = PathService(
            self.vision_service,
            self.communication_service,
            self.shortest_path_algorithm,
        )

        path_service.find_path_to_next_starting_zone_corner()

        self.a_starting_zone.find_corner_position_from_letter.assert_called_with(
            self.A_CORNER_LETTER
        )

    @patch.object(StartingZoneCorner, "get_next_corner")
    def test_givenTwoSuccessiveCalls_whenFindPathToNextStartingZoneCorner_thenCornerOrderIsFollowed(
        self, startingZoneCorner_mock
    ):
        self.vision_service.find_starting_zone.return_value = self.a_starting_zone
        self.communication_service.get_first_corner_letter.return_value = (
            self.A_CORNER_LETTER
        )
        startingZoneCorner_mock.return_value = self.ANOTHER_CORNER_LETTER
        path_service = PathService(
            self.vision_service,
            self.communication_service,
            self.shortest_path_algorithm,
        )

        path_service.find_path_to_next_starting_zone_corner()
        path_service.find_path_to_next_starting_zone_corner()

        self.a_starting_zone.find_corner_position_from_letter.assert_has_calls(
            self.a_starting_zone.find_corner_position_from_letter(self.A_CORNER_LETTER),
            self.a_starting_zone.find_corner_position_from_letter(
                self.ANOTHER_CORNER_LETTER
            ),
        )

    def test_whenFindPathToNextStartingZoneCorner_thenPathIsCalculatedWithRightCornerPositionAndRobotPosition(
        self,
    ):
        self.a_starting_zone.find_corner_position_from_letter = MagicMock(
            return_value=self.A_CORNER_POSITION
        )
        self.vision_service.find_robot_position = MagicMock(
            return_value=self.A_ROBOT_POSITION
        )
        self.vision_service.find_starting_zone.return_value = self.a_starting_zone
        path_service = PathService(
            self.vision_service,
            self.communication_service,
            self.shortest_path_algorithm,
        )

        path_service.find_path_to_next_starting_zone_corner()

        self.shortest_path_algorithm.find_shortest_path.assert_called_with(
            self.A_ROBOT_POSITION, self.A_CORNER_POSITION
        )
