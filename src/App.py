from context.StationContext import StationContext


class App:
    @staticmethod
    def run(local_flag):
        StationContext(local_flag).run()
