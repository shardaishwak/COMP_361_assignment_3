import sys
import math
import heapq
from typing import List, Tuple, Optional, Set, Deque
from enum import Enum
from collections import deque

class Node:
    """
    A generic Node that can be used by A*, Dijkstra, or GrassFire (BFS).
    For convenience, we store multiple fields:
      - g, f, h for A*
      - cost for Dijkstra
      - value for GrassFire
      - parent for path reconstruction
    """
    def __init__(self, node_id=0, h=0.0):
        self.id = node_id
        
        # For A*
        self.g = math.inf
        self.f = math.inf
        self.h = h
        
        # For Dijkstra
        self.cost = math.inf
        
        # For GrassFire (BFS)
        self.value = -1   # unvisited = -1, or 0-based distance
        
        self.parent: Optional["Node"] = None
        
        # neighbors: set of (neighbor_node, weight)
        self.neighbors: Set[Tuple["Node", float]] = set()

    def __lt__(self, other: "Node"):
        """
        Needed so we can push Node directly into a priority queue (heapq)
        under A* or Dijkstra. By default, compare by f (A*) or cost (Dijkstra).
        We'll use A*'s f primarily; for Dijkstra, we can treat cost as f or g.
        """
        # If you're strictly using A*, you'd compare by self.f.
        # If you're strictly using Dijkstra, you'd compare by self.cost.
        # We'll pick self.f to keep it simple for A*. If doing Dijkstra,
        # we will manually use cost instead of f in the priority queue logic.
        return self.f < other.f

    def reset_for_astar(self):
        """Reset fields used by A*."""
        self.g = math.inf
        self.f = math.inf
        self.parent = None

    def reset_for_dijkstra(self):
        """Reset fields used by Dijkstra."""
        self.cost = math.inf
        self.parent = None

    def reset_for_grassfire(self):
        """Reset fields used by GrassFire (BFS)."""
        self.value = -1
        self.parent = None


class Status(Enum):
    END = "END"
    CONTINUE = "CONTINUE"


class PriorityQueue:
    """
    Simple min-heap for Node objects (used by A* or Dijkstra).
    If used with Dijkstra, we might store (cost, node) manually
    instead of using node.f.
    """
    def __init__(self):
        self.queue: List[Node] = []

    def push(self, node: Node):
        heapq.heappush(self.queue, node)

    def pop(self) -> Node:
        return heapq.heappop(self.queue)

    def remove(self, node: Node):
        # O(n) removal from heap list; then must re-heapify
        self.queue.remove(node)
        heapq.heapify(self.queue)

    def has(self, node: Node) -> bool:
        return node in self.queue

    def empty(self) -> bool:
        return len(self.queue) == 0
