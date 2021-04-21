import time

from context.RobotContext import RobotContext

if __name__ == "__main__":
    context = RobotContext(False)
    while True:
        context._communication_service.send_gripper_status()
        time.sleep(0.2)