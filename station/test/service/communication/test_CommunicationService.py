from unittest import TestCase
from unittest.mock import MagicMock

from service.communication.CommunicationService import CommunicationService


class TestCommunicationService(TestCase):
    A_MESSAGE = "a message"
    SOCKET_ADDRESS = "a socket address"
    A_PATH = MagicMock()

    def setUp(self):
        self.game_cycle_connector = MagicMock()
        self.robot_update_connector = MagicMock()
        self.communication_service = CommunicationService(
            self.game_cycle_connector, self.robot_update_connector
        )

    def test_givenStatusPublishedByRobot_whenReceiveRobotStatus_thenStatusConnectorReceivesMessage(
        self,
    ):
        self.communication_service.receive_robot_status()

        self.robot_update_connector.read_all_topics.assert_called()

    def test_whenSendGameCycleRequest_thenGameCycleConnectorSendsMessage(self):
        self.communication_service.send_game_cycle_response(self.A_MESSAGE)

        self.game_cycle_connector.send_message.assert_called()

    def test_givenGameCycleMessageSentByRobot_whenSendGameCycleRequest_thenGameCycleConnectorReceivesMessage(
        self,
    ):
        self.communication_service.receive_game_cycle_request()

        self.game_cycle_connector.receive_message.assert_called()

    def test_givenAnObject_whenSendObject_thenObjectIsSerializedAndSent(self):
        self.communication_service.send_object(self.A_PATH)

        self.game_cycle_connector.send_object.assert_called_with(self.A_PATH)

    def test_whenReceiveObject_thenObjectIsDeserializedAndReturned(self):
        an_object = MagicMock()
        self.game_cycle_connector.receive_object.return_value = an_object

        actual_object = self.communication_service.receive_object()

        self.assertEqual(an_object, actual_object)

    def test_whenReceiveGripperStatus_thenGripperTopicIsRead(self):
        self.communication_service.receive_gripper_status()

        self.robot_update_connector.read_topic.assert_called_with("gripper_status")

    def test_givenGripperStatusSentByRobot_whenReceiveGripperStatus_thenGripperStatusIsReturned(
        self,
    ):
        expected_gripper_status = 1
        self.robot_update_connector.read_topic.return_value = expected_gripper_status

        actual_gripper_status = self.communication_service.receive_gripper_status()
        self.assertEqual(expected_gripper_status, actual_gripper_status)

    def test_whenReceivePowerConsumption_thenPowerConsumptionTopicIsRead(self):
        self.communication_service.receive_power_consumption()

        self.robot_update_connector.read_topic.assert_called_with("power_consumption")

    def test_givenPowerConsumptionSentByRobot_whenReceivePowerConsumption_thenPowerConsumptionIsReturned(
        self,
    ):
        expected_power_consumption = 10.0
        self.robot_update_connector.read_topic.return_value = expected_power_consumption

        actual_power_consumption = (
            self.communication_service.receive_power_consumption()
        )
        self.assertEqual(expected_power_consumption, actual_power_consumption)

    def test_whenReceiveBatteryConsumption_thenBatteryConsumptionTopicIsRead(self):
        self.communication_service.receive_battery_consumption()

        self.robot_update_connector.read_topic.assert_called_with("battery_consumption")

    def test_givenBatteryConsumptionSentByRobot_whenReceiveBatteryConsumption_thenBatteryConsumptionIsReturned(
        self,
    ):
        expected_battery_consumption = 10.0
        self.robot_update_connector.read_topic.return_value = (
            expected_battery_consumption
        )

        actual_battery_consumption = (
            self.communication_service.receive_battery_consumption()
        )
        self.assertEqual(expected_battery_consumption, actual_battery_consumption)

    def test_whenReceiveBatteryTimeLeft_thenBatteryTimeLeftTopicIsRead(self):
        self.communication_service.receive_battery_time_left()

        self.robot_update_connector.read_topic.assert_called_with("battery_time_left")

    def test_givenBatteryTimeLeftSentByRobot_whenReceiveBatteryTimeLeft_thenBatteryTimeLeftIsReturned(
        self,
    ):
        expected_battery_time_left = 2000000.0000
        self.robot_update_connector.read_topic.return_value = expected_battery_time_left

        actual_battery_time_left = (
            self.communication_service.receive_battery_time_left()
        )
        self.assertEqual(expected_battery_time_left, actual_battery_time_left)

    def test_whenReceiveBatteryPercentage_thenBatteryPercentageTopicIsRead(self):
        self.communication_service.receive_battery_percentage()

        self.robot_update_connector.read_topic.assert_called_with("battery_percentage")

    def test_givenBatteryPercentageSentByRobot_whenReceiveBatteryPercentage_thenBatteryPercentageIsReturned(
        self,
    ):
        expected_battery_percentage = 99.9949494
        self.robot_update_connector.read_topic.return_value = (
            expected_battery_percentage
        )

        actual_battery_percentage = (
            self.communication_service.receive_battery_percentage()
        )
        self.assertEqual(expected_battery_percentage, actual_battery_percentage)

    def test_whenReceivePowerConsumptionFirstWheel_thenPowerConsumptionFirstWheelTopicIsRead(
        self,
    ):
        self.communication_service.receive_power_consumption_first_wheel()

        self.robot_update_connector.read_topic.assert_called_with(
            "first_wheel_power_consumption"
        )

    def test_givenPowerConsumptionFirstWheelSentByRobot_whenReceivePowerConsumptionFirstWheel_thenPowerConsumptionFirstWheelIsReturned(
        self,
    ):
        expected_power_consumption_first_wheel = 10.0
        self.robot_update_connector.read_topic.return_value = (
            expected_power_consumption_first_wheel
        )

        actual_power_consumption_first_wheel = (
            self.communication_service.receive_power_consumption_first_wheel()
        )
        self.assertEqual(
            expected_power_consumption_first_wheel, actual_power_consumption_first_wheel
        )

    def test_whenReceivePowerConsumptionSecondWheel_thenPowerConsumptionSecondWheelTopicIsRead(
        self,
    ):
        self.communication_service.receive_power_consumption_second_wheel()

        self.robot_update_connector.read_topic.assert_called_with(
            "second_wheel_power_consumption"
        )

    def test_givenPowerConsumptionSecondWheelSentByRobot_whenReceivePowerConsumptionSecondWheel_thenPowerConsumptionSecondWheelIsReturned(
        self,
    ):
        expected_power_consumption_second_wheel = 10.0
        self.robot_update_connector.read_topic.return_value = (
            expected_power_consumption_second_wheel
        )

        actual_power_consumption_second_wheel = (
            self.communication_service.receive_power_consumption_second_wheel()
        )
        self.assertEqual(
            expected_power_consumption_second_wheel,
            actual_power_consumption_second_wheel,
        )

    def test_whenReceivePowerConsumptionThirdWheel_thenPowerConsumptionThirdWheelTopicIsRead(
        self,
    ):
        self.communication_service.receive_power_consumption_third_wheel()

        self.robot_update_connector.read_topic.assert_called_with(
            "third_wheel_power_consumption"
        )

    def test_givenPowerConsumptionThirdWheelSentByRobot_whenReceivePowerConsumptionThirdWheel_thenPowerConsumptionThirdWheelIsReturned(
        self,
    ):
        expected_power_consumption_third_wheel = 10.0
        self.robot_update_connector.read_topic.return_value = (
            expected_power_consumption_third_wheel
        )

        actual_power_consumption_third_wheel = (
            self.communication_service.receive_power_consumption_third_wheel()
        )
        self.assertEqual(
            expected_power_consumption_third_wheel, actual_power_consumption_third_wheel
        )

    def test_whenReceivePowerConsumptionFourthWheel_thenPowerConsumptionFourthWheelTopicIsRead(
        self,
    ):
        self.communication_service.receive_power_consumption_fourth_wheel()

        self.robot_update_connector.read_topic.assert_called_with(
            "fourth_wheel_power_consumption"
        )

    def test_givenPowerConsumptionFourthWheelSentByRobot_whenReceivePowerConsumptionFourthWheel_thenPowerConsumptionFourthWheelIsReturned(
        self,
    ):
        expected_power_consumption_fourth_wheel = 10.0
        self.robot_update_connector.read_topic.return_value = (
            expected_power_consumption_fourth_wheel
        )

        actual_power_consumption_fourth_wheel = (
            self.communication_service.receive_power_consumption_fourth_wheel()
        )
        self.assertEqual(
            expected_power_consumption_fourth_wheel,
            actual_power_consumption_fourth_wheel,
        )
