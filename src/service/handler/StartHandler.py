from typing import Any

from domain.communication.Message import Message
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from service.communication.CommunicationService import CommunicationService
from service.exception.StageComplete import StageComplete
from service.gripper.GripperService import GripperService


class StartHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        gripper_service: GripperService,
    ):
        self._communication_service = communication_service
        self._gripper_service = gripper_service

    def execute(self):
        while True:
            try:
                self._route_station_command()
            except StageComplete:
                break

    def _route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()

        if topic == Topic.START_STAGE:
            self._gripper_service.elevate_gripper()
            self._send_confirmation_to_station(Topic.START_STAGE, Stage.STAGE_COMPLETED)

        else:
            print("wrong command")

    def _send_confirmation_to_station(self, topic: Topic, payload: Any):
        message = Message(topic, payload)
        self._communication_service.send_object(message)
        raise StageComplete
