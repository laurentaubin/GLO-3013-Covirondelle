from domain.gripper.GripperStatus import GripperStatus


class FakeRobotInformation:
    def get_gripper_status(self) -> GripperStatus:
        return GripperStatus.HAS_PUCK

    def get_current_consumption(self) -> float:
        return 10.0

    def get_power_consumption(self):
        return 12.0
