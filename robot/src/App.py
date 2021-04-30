from context.RobotContext import RobotContext


class App:
    @staticmethod
    def run(local_flag):
        RobotContext(local_flag).run()
