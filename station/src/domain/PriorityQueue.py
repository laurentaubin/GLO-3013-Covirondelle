import heapq
from re import T
from typing import Tuple, List


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]
