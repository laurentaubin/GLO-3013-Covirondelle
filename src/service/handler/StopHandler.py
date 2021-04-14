from typing import Any, List

from domain.Orientation import Orientation
from domain.communication.ILed import ILed
from domain.communication.Message import Message
from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.movement.Movement import Movement
from service.communication.CommunicationService import CommunicationService
from service.exception.StageComplete import StageComplete
from service.movement.MovementService import MovementService


class StopHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        movement_service: MovementService,
        led: ILed,
    ):
        self._communication_service = communication_service
        self._movement_service = movement_service
        self._led = led

    def execute(self):
        while True:
            try:
                self._route_station_command()
            except StageComplete:
                break

    def _route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()

        if topic == Topic.START_CYCLE:
            self._send_confirmation_to_station(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)

        elif topic == Topic.MOVEMENTS:
            self._move(command.get_payload())
            self._send_confirmation_to_station(Topic.MOVEMENTS, Stage.STAGE_COMPLETED)

        elif topic == Topic.ROTATION:
            self._rotate(command.get_payload())
            self._send_confirmation_to_station(Topic.ROTATION, Stage.STAGE_COMPLETED)

        elif topic == Topic.TURN_LED_ON:
            self._led.toggle_led()
            self._send_confirmation_to_station(Topic.TURN_LED_ON, Stage.STAGE_COMPLETED)

        elif topic == Topic.STAGE_COMPLETED:
            self._send_confirmation_to_station(
                Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
            )
            raise StageComplete

    def _send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def _rotate(self, orientation: Orientation):
        self._movement_service.rotate(orientation.get_orientation_in_degree())

    def _move(self, movements: List[Movement]):
        self._movement_service.move(movements)
