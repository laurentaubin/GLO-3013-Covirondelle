from typing import Any

from IntegrationContext import IntegrationContext

from domain.Orientation import Orientation
from domain.communication.Message import Message
from domain.game.Topic import Topic

USE_REAL_MOVEMENTS = False
ALIGN_WITH_COMMAND_PANEL_FOR_REAL = True


class ReadCommandPanelIT(IntegrationContext):
    def __init__(self):
        super().__init__(local_flag=False)

    def route_station_command(self):
        self.align_with_command_panel(0)
        raise Exception
        # command: Message = self._communication_service.receive_object()
        # topic = command.get_topic()
        # print(topic)
        # print(command.get_payload())
        #
        # if topic == Topic.START_STAGE:
        #     print("Stage started")
        #     self.send_confirmation_to_station(
        #         Topic.START_STAGE, Stage.READ_COMMAND_PANEL
        #     )
        #
        # elif topic == Topic.MOVEMENTS:
        #     print("Moving to puck")
        #     self.move(command.get_payload())
        #     print("Sending movement confirmation")
        #     grab_puck_it.send_confirmation_to_station(
        #         Topic.MOVEMENTS, Stage.STAGE_COMPLETED
        #     )
        #
        # elif topic == Topic.ROTATION:
        #     print("Rotating")
        #     self.rotate(command.get_payload())
        #
        #     print("Sending rotation confirmation")
        #     grab_puck_it.send_confirmation_to_station(
        #         Topic.ROTATION, Stage.STAGE_COMPLETED
        #     )
        #
        # elif topic == Topic.ANALYZE_COMMAND_PANEL:
        #     print("Analyzing command panel")
        #     self._align_with_command_panel()
        #
        # elif topic == Topic.STAGE_COMPLETED:
        #     print("Stage completed")
        #     self.send_confirmation_to_station(
        #         Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
        #     )
        #     raise RuntimeError("Stage complete !")

    def send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def move(self, movements):
        if USE_REAL_MOVEMENTS:
            self._movement_service._move(movements)
        else:
            print("Déplacez manuellement le robot près de la rondelle Jaune")
            input("Appuyez sur Entrer lorsque c'est fait")

    def align_with_command_panel(self, letter_position: int):
        if ALIGN_WITH_COMMAND_PANEL_FOR_REAL:
            first_starting_zone_corner = (
                self._read_command_panel_handler._read_command_panel(letter_position)
            )
            print(first_starting_zone_corner)
            # self._communication_service.send_object(
            #     Message(Topic.ANALYZE_COMMAND_PANEL, first_starting_zone_corner)
            # )
        else:
            print("On aligne pas pour de vrai")
            input("Appuyez sur Entrer pour envoyer D")
            self._communication_service.send_object(
                Message(Topic.ANALYZE_COMMAND_PANEL, "D")
            )

    def _align_with_command_panel(self):
        self._read_command_panel_handler._read_command_panel()

    def rotate(self, orientation: Orientation):
        self._movement_service._rotate(orientation.get_orientation_in_degree())


if __name__ == "__main__":
    grab_puck_it = ReadCommandPanelIT()
    while True:
        try:
            print("Waiting for next command")
            grab_puck_it.route_station_command()
        except Exception:
            break
