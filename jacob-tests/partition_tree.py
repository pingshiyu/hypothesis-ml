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
    
    def show(self, indent : int = 0):
        return f"[{str(self)}]"

class PNode:
    # children are of type: PNode | PLeaf
    def __init__(self, parent : Optional[PNode] = None, label : Optional[int] = None, children : list[PNode | PLeaf] = []):
        self.parent = parent
        self.children = children
        self.label = label
    
    def down(self, label : Optional[int] = None) -> PNode:
        # go down a level. 
        # if label provided, check for duplicate with parent
        # this rules the case where a second label is used again 
        if label:
            labelled_children = {n.label : n for n in self.children}
            if label == self.label:
                print(f"repeat label called: {label}")
                return self
            elif label in labelled_children.keys():
                print(f"repeated label of child called: {label}")
                return labelled_children[label]
        subtree = PNode(self, label, [])
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
        return self.show(0)
        # return (f"PNode(label={self.label}; "
        #         f"parent={'yes' if self.parent else 'no'}; "
        #         f"children=[{', '.join(map(str, self.children))}])")
    
    @staticmethod
    def _show_indent(n = 0):
        return "  " * n
    
    def show(self, indent: int = 0) -> str:
        return (
            f"<{self.label}>\n"
            f"{'\n'.join(self._show_indent(indent+1) + '| ' + c.show(indent+1) for c in self.children)}"
        )