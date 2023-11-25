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