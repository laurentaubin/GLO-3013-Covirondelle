from context.RobotContext import RobotContext


class IntegrationContext(RobotContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)
