from typing import List

from domain.Position import Position


class Path:
    def __init__(self, path: List[Position]) -> None:
        self._path = path

    def __eq__(self, other: "Path"):
        return self._path == other._path
