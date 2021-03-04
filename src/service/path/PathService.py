from domain.StartingZoneCorner import StartingZoneCorner
from domain.pathfinding.IShortestPathAlgorithm import IShortestPathAlgorithm
from domain.pathfinding.Path import Path
from service.communication.CommunicationService import CommunicationService
from service.vision import VisionService


class PathService:
    def __init__(
        self,
        vision_service: VisionService,
        communication_service: CommunicationService,
        shortest_path_algorithm: IShortestPathAlgorithm,
    ) -> None:
        self._vision_service = vision_service
        self._game_table = vision_service.create_game_table()
        self._communication_service = communication_service
        self._shortest_path_algorithm = shortest_path_algorithm
        self._current_corner_letter = (
            self._communication_service.get_first_corner_letter()
        )
        self._shortest_path_algorithm.set_maze(self._game_table.get_maze())

    def find_path_to_next_starting_zone_corner(self) -> Path:
        current_robot_position = self._vision_service.find_robot_position()
        corner_position = (
            self._game_table.get_starting_zone().find_corner_position_from_letter(
                self._current_corner_letter
            )
        )

        self._current_corner_letter = StartingZoneCorner.get_next_corner(
            self._current_corner_letter
        )

        return self._shortest_path_algorithm.find_shortest_path(
            current_robot_position, corner_position
        )
