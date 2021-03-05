import time

from domain.game.IStageHandler import IStageHandler
from service.communication.CommunicationService import CommunicationService
from service.mouvement.MovementService import MovementService
from service.resistance.ResistanceService import ResistanceService


class GoToOhmmeterHandler(IStageHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        movement_service: MovementService,
        resistance_service: ResistanceService,
    ):
        self.communication_service = communication_service
        self.movement_service = movement_service
        self.resistance_service = resistance_service

    def execute(self):
        print("In GoToOhmmeterHandler, doing stuff, waiting 3 sec")
        time.sleep(3)
