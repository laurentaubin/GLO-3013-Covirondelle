from unittest import TestCase
from unittest.mock import Mock

from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = "a message"
    SOCKET_ADDRESS = "a socket address"

    def setUp(self):
        self.game_cycle_connector = Mock()
        self.robot_update_connector = Mock()
        self.communicationService = CommunicationService(
            self.game_cycle_connector, self.robot_update_connector
        )

    def test_givenStatusPublishedByRobot_whenReceiveRobotStatus_thenStatusConnectorReceivesMessage(
        self,
    ):
        self.communicationService.receive_robot_status()

        self.assertTrue(self.robot_update_connector.receive_message.called)

    def test_whenSendGameCycleRequest_thenGameCycleConnectorSendsMessage(self):
        self.communicationService.send_game_cycle_response(self.A_MESSAGE)

        self.game_cycle_connector.send_message.assert_called()

    def test_givenGameCycleMessageSentByRobot_whenSendGameCycleRequest_thenGameCycleConnectorReceivesMessage(
        self,
    ):
        self.communicationService.receive_game_cycle_request()

        self.game_cycle_connector.receive_message.assert_called()
