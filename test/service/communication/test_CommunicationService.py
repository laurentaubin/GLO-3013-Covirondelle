from unittest import TestCase
from unittest.mock import MagicMock

from domain.communication.Message import Message
from domain.game.Topic import Topic
from domain.gripper.GripperStatus import GripperStatus
from service.communication.CommunicationService import CommunicationService

STATUS_HAS_PUCK = GripperStatus.HAS_PUCK

A_CURRENT_VALUE = 10.0

A_POWER_CONSUMPTION = 10.0

A_POWER_CONSUMPTION_FIRST_WHEEL = 5.0
A_POWER_CONSUMPTION_SECOND_WHEEL = 5.0
A_POWER_CONSUMPTION_THIRD_WHEEL = 5.0
A_POWER_CONSUMPTION_FOURTH_WHEEL = 5.0


class TestCommunicationService(TestCase):
    A_MESSAGE = Message(Topic.READ_RESISTANCE, False)

    def setUp(self):
        self.pub_sub_connector = MagicMock()
        self.game_cycle_connector = MagicMock()
        self.robot_information = MagicMock()
        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.pub_sub_connector, self.robot_information
        )

    def test_whenReceiveMessage_thenConnectorReceivesMessage(self):
        self.communication_service.receive_game_cycle_message()

        self.assertTrue(self.game_cycle_connector.receive_message.called)

    def test_whenSendMessage_thenConnectorSendsMessage(self):
        self.communication_service.send_game_cycle_message(self.A_MESSAGE)

        self.assertTrue(
            self.game_cycle_connector.send_message.called_with(self.A_MESSAGE)
        )

    def test_whenReceiveObject_thenConnectorIsUsedToReceiveObject(self):
        an_object = MagicMock()
        self.game_cycle_connector.receive_object.return_value = an_object

        actual_object = self.communication_service.receive_object()

        self.assertEqual(an_object, actual_object)

    def test_givenStatusReturnByRobotInformation_whenSendGripperStatus_thenPublishStatus(
        self,
    ):
        self.robot_information.get_gripper_status.return_value = STATUS_HAS_PUCK

        self.communication_service.send_gripper_status()

        self.pub_sub_connector.publish_gripper_status.assert_called_with(
            STATUS_HAS_PUCK
        )

    def test_givenCurrentConsumptionReturnedByRobotInformation_whenSendPowerConsumption_thenPublishCurrentConsumption(
        self,
    ):
        self.robot_information.get_current_consumption.return_value = A_CURRENT_VALUE
        self.communication_service.send_current_consumption()
        self.pub_sub_connector.publish_current_consumption.assert_called_with(
            A_CURRENT_VALUE
        )

    def test_givenPowerConsumptionReturnedByRobotInformation_whenSendPowerConsumption_thenPublishPowerConsumption(
        self,
    ):
        self.robot_information.get_power_consumption.return_value = A_POWER_CONSUMPTION

        self.communication_service.send_power_consumption()

        self.pub_sub_connector.publish_power_consumption.assert_called_with(
            A_POWER_CONSUMPTION
        )

    def test_givenPowerConsumptionFirstWheelReturnedByRobotInformation_whenSendPowerConsumptionFirstWheel_thenPublishPowerConsumptionFirstWheel(
        self,
    ):
        self.robot_information.get_power_consumption_first_wheel.return_value = (
            A_POWER_CONSUMPTION_FIRST_WHEEL
        )

        self.communication_service.send_power_consumption_first_wheel()

        self.pub_sub_connector.publish_power_consumption_first_wheel.assert_called_with(
            A_POWER_CONSUMPTION_FIRST_WHEEL
        )

    def test_givenPowerConsumptionSecondWheelReturnedByRobotInformation_whenSendPowerConsumptionSecondWheel_thenPublishPowerConsumptionSecondWheel(
        self,
    ):
        self.robot_information.get_power_consumption_second_wheel.return_value = (
            A_POWER_CONSUMPTION_SECOND_WHEEL
        )

        self.communication_service.send_power_consumption_second_wheel()

        self.pub_sub_connector.publish_power_consumption_second_wheel.assert_called_with(
            A_POWER_CONSUMPTION_SECOND_WHEEL
        )

    def test_givenPowerConsumptionThirdWheelReturnedByRobotInformation_whenSendPowerConsumptionThirdWheel_thenPublishPowerConsumptionThirdWheel(
        self,
    ):
        self.robot_information.get_power_consumption_third_wheel.return_value = (
            A_POWER_CONSUMPTION_THIRD_WHEEL
        )

        self.communication_service.send_power_consumption_third_wheel()

        self.pub_sub_connector.publish_power_consumption_third_wheel.assert_called_with(
            A_POWER_CONSUMPTION_THIRD_WHEEL
        )

    def test_givenPowerConsumptionFourthWheelReturnedByRobotInformation_whenSendPowerConsumptionFourthWheel_thenPublishPowerConsumptionFourthWheel(
        self,
    ):
        self.robot_information.get_power_consumption_fourth_wheel.return_value = (
            A_POWER_CONSUMPTION_FOURTH_WHEEL
        )

        self.communication_service.send_power_consumption_fourth_wheel()

        self.pub_sub_connector.publish_power_consumption_fourth_wheel.assert_called_with(
            A_POWER_CONSUMPTION_FOURTH_WHEEL
        )
