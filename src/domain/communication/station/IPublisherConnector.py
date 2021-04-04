class IPublisherConnector:
    def publish_message(self, message: str) -> None:
        pass

    def publish_gripper_status(self, gripper_status):
        pass

    def publish_current_consumption(self, current_consumption):
        pass

    def publish_power_consumption(self, power_consumption_status):
        pass
