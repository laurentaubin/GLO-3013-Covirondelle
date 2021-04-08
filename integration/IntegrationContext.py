from context.RobotContext import RobotContext
from domain.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from domain.Color import Color
from service.communication.CommunicationService import CommunicationService
from service.handler.TransportPuckHandler import TransportPuckHandler
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class FakePuckHandler(TransportPuckHandler):
    def __init__(
        self,
        communication_service: CommunicationService,
        vision_service: VisionService,
        movement_service: MovementService,
        puck_alignment_corrector: PuckAlignmentCorrector,
    ):
        super().__init__(
            communication_service,
            vision_service,
            movement_service,
            puck_alignment_corrector,
        )

    def align_with_puck(self, color: Color):
        self._align_with_puck(color)


class IntegrationContext(RobotContext):
    def __init__(self, local_flag):
        super().__init__(local_flag)
        self._puck_handler = FakePuckHandler(
            self._communication_service,
            self._vision_service,
            self._movement_service,
            self._puck_alignment_corrector,
        )
