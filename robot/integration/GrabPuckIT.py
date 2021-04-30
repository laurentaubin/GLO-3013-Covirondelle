from typing import Any
import time

from domain.Orientation import Orientation
from domain.communication.Message import Message
from domain.game.Stage import Stage
from domain.game.Topic import Topic
from domain.Color import Color
from IntegrationContext import IntegrationContext

PUCK_COLOR_TO_USE = Color.YELLOW
USE_REAL_MOVEMENTS = True
ALIGN_WITH_PUCK_FOR_REAL = True
ALIGN_WITH_STARTING_ZONE_FOR_REAL = True
GRAB_PUCK_FOR_REAL = True
DROP_PUCK_FOR_REAL = True


class GrabPuckIT(IntegrationContext):
    def __init__(self):
        super().__init__(local_flag=False)

    def route_station_command(self):
        command: Message = self._communication_service.receive_object()
        topic = command.get_topic()

        if topic == Topic.START_CYCLE:
            print("Stage started")
            self.send_confirmation_to_station(Topic.START_CYCLE, Stage.TRANSPORT_PUCK)

        elif topic == Topic.MOVEMENTS:
            print("Moving to puck")
            self.move(command.get_payload())

            print("Sending movement confirmation")
            grab_puck_it.send_confirmation_to_station(
                Topic.MOVEMENTS, Stage.STAGE_COMPLETED
            )

        elif topic == Topic.ROTATION:
            print("Rotating")
            self.rotate(command.get_payload())

            print("Sending rotation confirmation")
            grab_puck_it.send_confirmation_to_station(
                Topic.ROTATION, Stage.STAGE_COMPLETED
            )

        elif topic == Topic.GRAB_PUCK:
            print("Grabbing puck")
            self.grab_puck(Color.value_of_resistance_digit(command.get_payload()))

            print("Sending grab puck confirmation to station")
            grab_puck_it.send_confirmation_to_station(
                Topic.GRAB_PUCK, Stage.STAGE_COMPLETED
            )

        elif topic == Topic.DROP_PUCK:
            print("Dropping puck")
            self.drop_puck()

            print("Sending drop puck confirmation to station")
            grab_puck_it.send_confirmation_to_station(
                Topic.DROP_PUCK, Stage.STAGE_COMPLETED
            )

        elif topic == Topic.STAGE_COMPLETED:
            print("Stage completed")
            self.send_confirmation_to_station(
                Topic.STAGE_COMPLETED, Stage.TRANSPORT_PUCK
            )
            raise RuntimeError("Stage complete !")

    def send_confirmation_to_station(self, command: Topic, payload: Any):
        message = Message(command, payload)
        self._communication_service.send_object(message)

    def grab_puck(self, puck_color: Color):
        self._vision_service.make_camera_look_down()
        time.sleep(0.2)
        self.open_gripper()
        self.align_with_puck(puck_color)

        if GRAB_PUCK_FOR_REAL:
            self._gripper_service.close_gripper()
            time.sleep(1)
            self._gripper_service.elevate_gripper()
        else:
            print("Placez la rondelle dans le préhenseur et soulevez le")
            input("Appuyez sur Entrer lorsque c'est fait")

    def move(self, movements):
        if USE_REAL_MOVEMENTS:
            self._movement_service._move(movements)
        else:
            print("Déplacez manuellement le robot près de la rondelle Jaune")
            input("Appuyez sur Entrer lorsque c'est fait")

    def align_with_puck(self, puck_color: Color):
        if ALIGN_WITH_PUCK_FOR_REAL:
            self._transport_puck_handler._align_with_puck(puck_color)
        else:
            print("Placez la rondelle devant le préhenseur")
            input("Appuyez sur Entrer lorsque c'est fait")

    def open_gripper(self):
        if GRAB_PUCK_FOR_REAL:
            self._gripper_service._open_gripper()
            self._gripper_service.lower_gripper()

    def align_with_starting_zone_corner(self):
        if ALIGN_WITH_STARTING_ZONE_FOR_REAL:
            self._transport_puck_handler._align_with_starting_zone_corner()
        else:
            print("Déplacez le robot sur le coin de la zone de départ")
            input("Appuyez sur Entrer lorsque c'est fait")

    def drop_puck(self):
        self.align_with_starting_zone_corner()

        if DROP_PUCK_FOR_REAL:
            self._gripper_service.lower_gripper()
            self._gripper_service._open_gripper()
        else:
            print("Descendre le préhenseur et ouvrez le")
            input("Appuyez sur Entrer lorsque c'est fait")

    def rotate(self, orientation: Orientation):
        self._movement_service._rotate(orientation.get_orientation_in_degree())


if __name__ == "__main__":
    grab_puck_it = GrabPuckIT()

    while True:
        print("Waiting for next command")
        grab_puck_it.route_station_command()
