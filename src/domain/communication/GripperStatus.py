from enum import IntEnum


class GripperStatus(IntEnum):
    HAS_PUCK = 1
    DOESNT_HAVE_PUCK = 0

    @staticmethod
    def valueOf(int_value: int) -> "GripperStatus":
        for gripper_status in GripperStatus:
            if int_value == gripper_status.value:
                return gripper_status
