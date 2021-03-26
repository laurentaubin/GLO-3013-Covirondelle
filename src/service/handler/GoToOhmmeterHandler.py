from typing import List

from domain.game.IStageHandler import IStageHandler
from domain.game.Stage import Stage
from domain.movement.Movement import Movement
from domain.resistance.Resistance import Resistance
from service.communication.CommunicationService import CommunicationService
from service.movement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService


class GoToOhmmeterHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        movement_service: MovementService,
        resistance_service: ResistanceService,
    ):
        self._communication_service = communication_service
        self._movement_service = movement_service
        self._resistance_service = resistance_service

    def execute(self):
        self._communication_service.send_game_cycle_message(Stage.GO_TO_OHMMETER.value)

        movements: List[Movement] = self._communication_service.receive_object()
        self._movement_service.move(movements)
        resistance_value: Resistance = (
            self._resistance_service.take_resistance_measurement()
        )
        self._communication_service.send_object(resistance_value)

        self._route_station_response()
        self._communication_service.send_game_cycle_message(Stage.STAGE_COMPLETED.value)

    def _route_station_response(self):
        game_cycle = self._communication_service.receive_game_cycle_message()

        if game_cycle == Stage.STAGE_COMPLETED.value:
            pass
        else:
            print("whoops")
