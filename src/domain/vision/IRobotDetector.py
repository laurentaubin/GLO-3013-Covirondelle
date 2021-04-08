from domain.RobotPose import RobotPose


class IRobotDetector:
    def detect(self, image) -> RobotPose:
        pass
