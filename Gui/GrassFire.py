from collections import deque
from typing import Deque, List
from Node import Node

class GrassFire:
    """Breadth-first search (BFS)."""
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.queue: Deque[Node] = deque()

        self.start.value = 0
        self.queue.append(self.start)

    def run(self):
        while self.queue:
            current = self.queue.popleft()
            if current == self.goal:
                return  # Found path

            for neighbor, _weight in current.neighbors:
                # GrassFire doesn't use weight for BFS
                if neighbor.value == -1:  # unvisited
                    neighbor.value = current.value + 1
                    neighbor.parent = current
                    self.queue.append(neighbor)

    def reconstruct_path(self) -> List[Node]:
        path = []
        node = self.goal
        while node is not None:
            path.append(node)
            # Go to the parent
            node = node.parent
        path.reverse()
        return path
