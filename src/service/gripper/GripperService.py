from domain.IGripper import IGripper


class GripperService:
    def __init__(self, gripper: IGripper):
        self._gripper = gripper

    def open_gripper(self):
        self._gripper.open()

    def close_gripper(self):
        self._gripper.close()

    def elevate_gripper(self):
        self._gripper.elevate()

    def lower_gripper(self):
        self._gripper.lower()
