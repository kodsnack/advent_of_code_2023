from dataclasses import dataclass


@dataclass
class Path:
    path: list['Edge']
    goal: 'Node'
    cost: int

    def full_transition(self):
        return ''.join(edge.transition for edge in self.path)
    

@dataclass
class Node:
    label: object
    previous: 'Edge' = None

    def generate_path(self):
        p = Path([], self, 0)

        node = self

        while node.previous:
            p.cost += node.previous.cost
            p.path.append(node.previous)
            node = node.previous.start

        p.path.reverse()

        return p

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