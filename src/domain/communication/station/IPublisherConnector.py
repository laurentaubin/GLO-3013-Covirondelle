class IPublisherConnector:
    def publish_message(self, message: str) -> None:
        pass

    def publish_gripper_status(self, gripper_status):
        pass
