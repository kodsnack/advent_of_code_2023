from dataclasses import dataclass

from edge import Edge
from node import Node


@dataclass
class Path:
    path: list[Edge]
    goal: Node
    cost: int

    def full_transition(self):
        return ''.join(edge.transition for edge in self.path)