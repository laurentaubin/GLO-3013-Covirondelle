class IPublisherConnector:
    def publish_message(self, message: str) -> None:
        pass

    def publish_gripper_status(self, gripper_status):
        pass

    def publish_current_consumption(self, current_consumption):
        pass

    def publish_power_consumption(self, power_consumption_status):
        pass

    def publish_power_consumption_first_wheel(self, power_consumption_first_wheel):
        pass

    def publish_power_consumption_second_wheel(self, power_consumption_second_wheel):
        pass

    def publish_power_consumption_third_wheel(self, power_consumption_third_wheel):
        pass

    def publish_power_consumption_fourth_wheel(self, power_consumption_fourth_wheel):
        pass
