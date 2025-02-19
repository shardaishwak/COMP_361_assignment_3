import math
import heapq
from typing import TypeVar, Generic, Set, Tuple
from enum import Enum

T = TypeVar('T')
S = TypeVar('S')


class Status(Enum):
    END = "END",
    CONTINUE = "CONTINUE"


class Node:
    def __init__(self, id = 0, h = 0):
        self.f = math.inf
        self.h = h
        self.g = math.inf
        self.id = id
        self.parent: Node = None
        self.neighbors: Set[Tuple[Node, int]] = set()

    def set_neighbors(self, *nodes: any):
        for node in nodes:
            self.neighbors.add(node)
    
    def get_neighbors(self):
        return self.neighbors
    
    def set_parent(self, node: any):
        self.parent = node
    
    def __repr__(self):
        return f"Node: {self.id}, f: {self.f}, g: {self.g}, h: {self.h}, neighbors: {str({n[0].id for n in self.neighbors})}"
    
    # Define comparison: for priority queue so that we do not need (f, Node), but just (Node)
    def __lt__(self, other: any):
        return self.f < other.f
    

class PriorityQueue(Generic[T]):
    def __init__(self):
        self.queue = []
    
    def push(self, value: T):
        heapq.heappush(self.queue, value)
    
    def pop(self) -> T:
        return heapq.heappop(self.queue)

    def remove(self, value: T):
        self.queue.remove(value)

    def has(self, value: T) -> bool:
        return value in self.queue
    
    def empty(self) -> bool:
        return len(self.queue) == 0
    
    def __repr__(self):
        return self.queue.__repr__()


class AStar:
    def __init__(self, start: Node, goal: Node):
        self.start = start
        self.start.g = 0
        self.goal = goal
        self.openSet = PriorityQueue[Node]()
        self.closeSet: Set[Node] = set()

    def step(self) -> Status:
        current = self.openSet.pop()

        if current == self.goal:
            return Status.END
        
        self.closeSet.add(current)

        neighbors = current.get_neighbors()
        for neighbor in neighbors:
            cost = current.g + neighbor[1]
            if cost < neighbor[0].g:
                neighbor[0].parent = current
                neighbor[0].f = cost + neighbor[0].h
                neighbor[0].g = cost
                
                if not self.openSet.has(neighbor[0]):
                    # remove it and then insert back because the f has changed
                    self.openSet.push(neighbor[0])
                else:
                    # pop from the queue and add it back since the f has changed
                    # this will update the priority queu
                    self.openSet.remove(neighbor[0])
                    self.openSet.push(neighbor[0])

        return Status.CONTINUE
    
    def run(self):
        self.openSet.push(self.start)
        while not self.openSet.empty():
            self.step()
    
    def reiterate(self) -> list[Node]:
        order = []
        node = self.goal
        while node is not None:
            order.append(node)
            node = node.parent

        order.reverse()
        return order
    

# Define nodes
node0 = Node(0, 20)
node1 = Node(1, 16)
node2 = Node(2, 6)
node3 = Node(3, 10)
node4 = Node(4, 4)
node5 = Node(5, 0)



# Create neighbors
node0.set_neighbors((node1, 2), (node3, 6))
node1.set_neighbors((node0, 2), (node2, 5))
node2.set_neighbors((node1, 5), (node3, 7), (node4, 6), (node5, 9))
node3.set_neighbors((node0, 6), (node2, 7), (node4, 10))
node4.set_neighbors((node2, 6), (node3, 10), (node4, 6))
node5.set_neighbors((node2, 9), (node4, 6))

# Just checking
# print(node0)
# print(node1)
# print(node2)
# print(node3)
# print(node4)
# print(node5)
        

# Run the algorithm
# algorithm = AStar(node0, node5)
# algorithm.run()

# print(algorithm.reconstruct())

# Traverse and find the route


