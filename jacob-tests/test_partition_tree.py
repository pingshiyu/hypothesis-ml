from partition_tree import PNode, PLeaf

import pytest

def test_partition_tree_single_print():
    t = PNode(None, 
              None,
              [
                  PNode(None, 10, [
                      PLeaf("x"), PLeaf("y")
                  ])
              ])
    expected = """<None>
  | <10>
    | [x]
    | [y]"""
    assert t.show() == expected

def test_parition_tree_multiple_children():
    t = PNode(None, 
              None,
              [
                  PNode(None, 10, [
                      PLeaf("x"), PLeaf("y")
                  ]),
                  PNode(None, 11, [
                      PLeaf("z"), PLeaf("w")
                  ])
              ])
    expected = """<None>
  | <10>
    | [x]
    | [y]
  | <11>
    | [z]
    | [w]"""
    assert t.show() == expected