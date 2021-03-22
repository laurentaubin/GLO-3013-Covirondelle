from unittest import TestCase
from unittest.mock import MagicMock

from service.handler.TransportPuckHandler import TransportPuckHandler


class TestTransportPuckHandler(TestCase):
    def setUp(self) -> None:
        self.vision_service = MagicMock()
        self.movement_service = MagicMock()

        self.transport_puck_handler = TransportPuckHandler(
            self.vision_service, self.movement_service
        )
