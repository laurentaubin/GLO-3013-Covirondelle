from unittest.mock import MagicMock

from domain.Orientation import Orientation
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from IntegrationContext import IntegrationContext

test_directions = [0, 180]


class RotationIT(IntegrationContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)

    def run(self):
        self._send_start_signal()
        self._route_robot_response()
        for dir in test_directions:
            self._rotation_service.rotate(Orientation(dir))

    def _send_start_signal(self):
        print("Sending start signal...")
        self._communication_service.send_object(
            Message(Topic.START_STAGE, Stage.START_CYCLE)
        )

    def _route_robot_response(self):
        message = self._communication_service.receive_object()
        if message.get_payload() == Stage.STAGE_COMPLETED:
            return
        print("Whoops, robot sent the wrong thing")


if __name__ == "__main__":
    rotation_it = RotationIT(local_flag=False)
    rotation_it.run()
