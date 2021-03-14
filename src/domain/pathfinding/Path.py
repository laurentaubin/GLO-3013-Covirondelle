from typing import List

from domain.Position import Position


class Path:
    def __init__(self, path: List[Position]) -> None:
        self._path = path

    def __eq__(self, other):
        if isinstance(other, Path):
            return self._path == other._path
        return False

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self._path):
            result = self._path[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration
