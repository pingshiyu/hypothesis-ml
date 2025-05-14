# a data structure that provides partitions on a random sequence
# data PTree a = PLeaf a | PNode [PTree a]

# with functions to go "deeper" and "shallowed" within the tree
# data PTree a = PLeaf {parent :: Maybe (PTree a), value :: a} | PNode {parent :: Maybe (PTree a), children :: [PTree a]}
# data PTree a = PTree {parent :: Maybe (PTree a), children :: [PTree a]}

# so every class object has a parent pointer, and children which are a python list of these class objects

from typing import Optional


class PNode:
    ...

class PLeaf:
    ...

class PLeaf:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class PNode:
    # children are of type: PNode | PLeaf
    def __init__(self, parent : Optional[PNode] = None, children : list[PNode | PLeaf] = []):
        self.parent = parent
        self.children = children
    
    def down(self) -> PNode:
        # go down a level. 
        subtree = PNode(self, [])
        self.children.append(subtree)
        return subtree
    
    def up(self) -> PNode:
        # go up a level
        if self.parent is None:
            raise Exception("No parent")
        return self.parent
    
    def add_value(self, value):
        self.children.append(PLeaf(value))

    def __str__(self):
        return f"PNode({', '.join(map(str, self.children))})"