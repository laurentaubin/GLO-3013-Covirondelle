import unittest
from unittest.mock import MagicMock, patch

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose
from domain.game.Stage import Stage
from domain.pathfinding.Path import Path
from domain.resistance.Resistance import Resistance
from service.handler.GoToOhmmeterHandler import GoToOhmmeterHandler


class TestGoToOhmmeterHandler(unittest.TestCase):
    A_ROBOT_POSITION = Position(1, 2)
    A_ROBOT_ORIENTATION = Orientation(2)
    A_ROBOT_POSE = RobotPose(A_ROBOT_POSITION, A_ROBOT_ORIENTATION)
    A_PATH = Path([A_ROBOT_POSITION])
    A_RESISTANCE = Resistance(123)
    SOME_MOVEMENTS = MagicMock()

    def setUp(self) -> None:
        self.communication_service = MagicMock()
        self.path_service = MagicMock()
        self.movement_factory = MagicMock()
        self.go_to_ohmmeter_handler = GoToOhmmeterHandler(
            self.communication_service, self.path_service, self.movement_factory
        )

    @patch("domain.game.GameState.GameState.set_current_stage")
    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_whenExecute_thenGameStateIsUpdatedWithGoToOhmmeterGameStage(
        self, gameState_mock
    ):
        go_to_ohmmeter_stage = Stage.GO_TO_OHMMETER

        self.go_to_ohmmeter_handler.execute()

        gameState_mock.assert_called_with(go_to_ohmmeter_stage)

    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenPath_whenExecute_thenSendGameCycleResponseToRobot(self):
        self.go_to_ohmmeter_handler.execute()

        number_of_calls = self.communication_service.send_game_cycle_response.call_count
        self.assertEqual(2, number_of_calls)

    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenGameStateUpdated_whenExecute_thenReceiveGameCycleIsCalled(self):
        self.go_to_ohmmeter_handler.execute()

        self.communication_service.receive_game_cycle_request.assert_called()

    @patch("domain.game.GameState.GameState.get_robot_pose")
    def test_whenExecute_thenRobotIsLocalised(self, gameStateRobotPose_mock):
        gameStateRobotPose_mock.return_value = self.A_ROBOT_POSE
        self.go_to_ohmmeter_handler.execute()
        gameStateRobotPose_mock.assert_called()

    @patch("domain.game.GameState.GameState.get_robot_pose")
    def test_givenRobotPose_whenExecute_thenPathServiceIsCalledWithCorrectPosition(
        self, gameStateRobotPose_mock
    ):
        gameStateRobotPose_mock.return_value = self.A_ROBOT_POSE

        self.go_to_ohmmeter_handler.execute()

        self.path_service.find_path_to_ohmmeter.assert_called_with(
            self.A_ROBOT_POSITION
        )

    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenPathToOhmmeter_whenExecute_thenMovementIsGeneratedFromPath(self):
        self.path_service.find_path_to_ohmmeter.return_value = self.A_PATH

        self.go_to_ohmmeter_handler.execute()

        self.movement_factory.create_movements.assert_called_with(self.A_PATH)

    @patch("domain.game.GameState.GameState.get_robot_pose")
    def test_givenPathToOhmmeter_whenExecute_thenResistanceValueIsReceivedFromRobot(
        self, gameStateRobotPose_mock
    ):
        gameStateRobotPose_mock.return_value = self.A_ROBOT_POSE

        self.go_to_ohmmeter_handler.execute()

        self.communication_service.receive_game_cycle_request.assert_called()

    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenPathToOhmmeter_whenExecute_thenSendObjectMovementsToRobot(self):
        self.movement_factory.create_movements.return_value = self.SOME_MOVEMENTS

        self.go_to_ohmmeter_handler.execute()

        self.communication_service.send_object.assert_called_with(self.SOME_MOVEMENTS)

    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenPathToOhmmeter_whenExecute_thenReceiveObjectWithPathIsCalled(self):
        self.go_to_ohmmeter_handler.execute()
        self.communication_service.receive_object.assert_called()

    @patch("domain.game.GameState.GameState.set_resistance_value")
    @patch(
        "domain.game.GameState.GameState.get_robot_pose",
        MagicMock(return_value=A_ROBOT_POSE),
    )
    def test_givenResistanceValue_whenExecute_thenResistanceIsSetInGameState(
        self, gameStateSetResistance
    ):
        self.communication_service.receive_object.return_value = self.A_RESISTANCE

        self.go_to_ohmmeter_handler.execute()

        gameStateSetResistance.assert_called_with(self.A_RESISTANCE)
