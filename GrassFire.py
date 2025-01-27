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
        self.value = 0
        self.neighbors: Set[Node] = set()

    def set_neighbors(self, *nodes: any):
        for node in nodes:
            self.neighbors.add(node)

    def get_neighbors(self):
        return self.neighbors
    
    def get_neighbor_with_smallest_value(self):
        if len(self.neighbors) == 0:
            # this means that we are at the root node
            # we assume no orphan node
            return None
        return min(*self.neighbors)
    
    def is_visited(self):
        return self.value > 0 

    def __repr__(self):
        return f"Node: {self.id}, Value: {self.value}, Neighbors: {str({n.id for n in self.get_neighbors()})}" 
    
    def __lt__(self, other: any):
        return self.value < other.value
    


class GrassFire:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.start.value = 0
        self.end = end
        self.queue = deque[Node]()

    def step(self):
        current = self.queue.pop()
        if current == self.end:
            return Status.END
        
        neighbors = current.get_neighbors()
        for neighbor in neighbors:
            
            if neighbor.is_visited() or neighbor == self.start:
                continue

            neighbor.value = current.value+1
            self.queue.append(neighbor)

    def reiterate(self) -> list[Node]:
        path = []
        node = self.end
        while node is not None and node is not self.start:
            path.append(node)
            node = node.get_neighbor_with_smallest_value()

        path.append(self.start)
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
node0.set_neighbors(node1, node3)
node1.set_neighbors(node0, node2)
node2.set_neighbors(node1, node3, node4, node5)
node3.set_neighbors(node0, node2, node4)
node4.set_neighbors(node2, node3, node4)
node5.set_neighbors(node2, node4)

# Just checking
print(node0)
print(node1)
print(node2)
print(node3)
print(node4)
print(node5)



algorithm = GrassFire(node0, node5)
algorithm.run()
path = algorithm.reiterate()

print(node0)
print(node1)
print(node2)
print(node3)
print(node4)
print(node5)



for node in path:
    print(node.id)




