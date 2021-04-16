import time

from domain.IGripper import IGripper


class GripperService:
    def __init__(self, gripper: IGripper):
        self._gripper = gripper

    def open_gripper(self):
        self._gripper.open()
        time.sleep(0.5)

    def close_gripper(self):
        self._gripper.close()
        time.sleep(0.5)

    def elevate_gripper(self):
        self._gripper.elevate()
        time.sleep(0.5)

    def lower_gripper(self):
        self._gripper.lower()
        time.sleep(0.5)
