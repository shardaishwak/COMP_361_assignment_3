import math
import heapq
from typing import TypeVar, Generic, Set, Tuple
from enum import Enum
from collections import deque


T = TypeVar('T')
S = TypeVar('S')


class Status(Enum):
    END = "END",
    CONTINUE = "CONTINUE"



class Node:
    def __init__(self, id = 0):
        self.id = id
        self.cost = math.inf
        self.parent: Node = None
        # (Node, weight)
        self.neighbors: list[Tuple[Node, int]] = set()

    def set_neighbors(self, *nodes: any):
        for node in nodes:
            self.neighbors.add(node)

    def get_neighbors(self):
        return self.neighbors
    
    def __repr__(self):
        return f"Node: {self.id}, Cost: {self.cost}, parent: {self.parent}, Neighbors: {str({n[0].id for n in self.get_neighbors()})}"
    


# in dikstra we run the algorithm until all the nodes have not been visited. No heuristics here.
class Dikstra:
    def __init__(self, start):
        self.start = start
        self.start.cost = 0
        self.queue = deque[Node]()
        self.visited: Set[Node] = set()

    def step(self):
        current = self.queue.pop()
        if current in self.visited:
            return Status.CONTINUE

        self.visited.add(current)

        neighbors = current.get_neighbors()

        for _neighbor in neighbors:
            neighbor, weight = _neighbor

            cost = current.cost + weight
            if cost < neighbor.cost:
                neighbor.cost = cost
                neighbor.parent = current
            
            self.queue.append(neighbor)
        
        return Status.CONTINUE
    
    def reiterate(self, goal: Node) -> list[Node]:
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = node.parent
        
        path.reverse()
        return path
    
    def run(self):
        self.queue.append(self.start)
        while len(self.queue) > 0:
            self.step()


node0 = Node(0)
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node5 = Node(5)


# Create neighbors
node0.set_neighbors((node1, 2), (node3, 6))
node1.set_neighbors((node0, 2), (node2, 5))
node2.set_neighbors((node1, 5), (node3, 7), (node4, 6), (node5, 9))
node3.set_neighbors((node0, 6), (node2, 7), (node4, 10))
node4.set_neighbors((node2, 6), (node3, 10), (node4, 6))
node5.set_neighbors((node2, 9), (node4, 6))

# Just checking
print(node0)
print(node1)
print(node2)
print(node3)
print(node4)
print(node5)



algorithm = Dikstra(node0)
algorithm.run()

path = algorithm.reiterate(node2)

for node in path:
    print(node.id)


