from domain.gripper.GripperStatus import GripperStatus


class IRobotInformation:
    def get_gripper_status(self) -> GripperStatus:
        pass
