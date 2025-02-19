import heapq
from Node import Node, PriorityQueue
from typing import List, Set, Tuple

class Dijkstra:
    """Dijkstra's algorithm for shortest path."""
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.goal = goal
        self.visited: Set[Node] = set()
        
        # Instead of using node.f, we'll store (cost, node) in the PriorityQueue
        self.queue = []
        heapq.heapify(self.queue)

        self.start.cost = 0
        heapq.heappush(self.queue, (self.start.cost, self.start))

    def run(self):
        while self.queue:
            current_cost, current = heapq.heappop(self.queue)
            if current == self.goal:
                return  # Found path

            if current in self.visited:
                continue
            self.visited.add(current)

            for neighbor, weight in current.neighbors:
                new_cost = current.cost + weight
                if new_cost < neighbor.cost:
                    neighbor.cost = new_cost
                    neighbor.parent = current
                    heapq.heappush(self.queue, (neighbor.cost, neighbor))

    def reconstruct_path(self) -> List[Node]:
        path = []
        node = self.goal
        while node is not None:
            path.append(node)
            node = node.parent
        path.reverse()
        return path

