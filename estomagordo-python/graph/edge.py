from dataclasses import dataclass


@dataclass
class Node:
    label: str
    previous: Edge = None

    def __hash__(self):
        return hash(self.label)
    
    def __eq__(self, other):
        return self.label == other.label
    
    def __lt__(self, other):
        return self.label < other.label


@dataclass
class Edge:
    start: Node
    end: Node
    cost: int
    bidirectional: bool = True
    transition: str = ''


@dataclass
class Path:
    path: list[Edge]
    goal: Node
    cost: int

    def full_transition(self):
        return ''.join(edge.transition for edge in self.path)