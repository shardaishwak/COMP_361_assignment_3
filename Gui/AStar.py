from Node import Node, PriorityQueue
from typing import List, Set, Tuple

class AStar:
    """A* search from start to goal."""
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.open_set = PriorityQueue()
        self.closed_set: Set[Node] = set()

        # Reset relevant fields
        # (Assume we did reset_for_astar externally if needed)
        self.start.g = 0
        self.start.f = self.start.h
        self.open_set.push(self.start)

    def run(self):
        while not self.open_set.empty():
            current = self.open_set.pop()

            if current == self.goal:
                return  # Found path

            self.closed_set.add(current)

            for neighbor, weight in current.neighbors:
                if neighbor in self.closed_set:
                    continue

                tentative_g = current.g + weight
                if tentative_g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = tentative_g
                    neighbor.f = neighbor.g + neighbor.h

                    if not self.open_set.has(neighbor):
                        self.open_set.push(neighbor)
                    else:
                        # Update neighbor in the priority queue
                        self.open_set.remove(neighbor)
                        self.open_set.push(neighbor)

    def reconstruct_path(self) -> List[Node]:
        path = []
        node = self.goal
        while node is not None:
            path.append(node)
            node = node.parent
        path.reverse()
        return path

