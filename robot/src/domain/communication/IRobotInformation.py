from domain.gripper.GripperStatus import GripperStatus


class IRobotInformation:
    def get_gripper_status(self) -> GripperStatus:
        pass

    def get_current_consumption(self) -> float:
        pass

    def get_power_consumption(self):
        pass

    def get_power_consumption_first_wheel(self):
        pass

    def get_power_consumption_second_wheel(self):
        pass

    def get_power_consumption_third_wheel(self):
        pass

    def get_power_consumption_fourth_wheel(self):
        pass

    def get_battery_time_left(self):
        pass

    def get_battery_percentage(self):
        pass
