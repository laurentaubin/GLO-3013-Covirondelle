from domain.communication.IRobotInformation import IRobotInformation
from domain.gripper.GripperStatus import GripperStatus


class FakeRobotInformation(IRobotInformation):
    def get_gripper_status(self) -> GripperStatus:
        return GripperStatus.HAS_PUCK

    def get_current_consumption(self) -> float:
        return 10.0

    def get_power_consumption(self):
        return 12.0

    def get_power_consumption_first_wheel(self):
        return 1.0

    def get_power_consumption_second_wheel(self):
        return 2.0

    def get_power_consumption_third_wheel(self):
        return 3.0

    def get_power_consumption_fourth_wheel(self):
        return 4.0

    def get_battery_time_left(self):
        return 123.4

    def get_battery_percentage(self):
        return 92.1
