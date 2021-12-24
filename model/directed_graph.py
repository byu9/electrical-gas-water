#!/usr/bin/env python3

class DirectedGraph:
    _parents = dict()
    _children = dict()
    _nodes = set()

    @property
    def nodes(self):
        return self._nodes

    def parents_of(self, node):
        yield from self._parents[node]

    def children_of(self, node):
        yield from self._children[node]

    def __init__(self, nodes):
        self._nodes = set(nodes)
        
        for node in self._nodes:
            self._children[node] = set()
            self._parents[node] = set()
        
    def add_children(self, node, children):
        children = set(children)
        
        if node not in self._nodes:
            raise ValueError('Adding children to a nonexistent node.')

        for child in children:
            if child not in self._nodes:
                raise ValueError('Nonexistent child.')

        self._children[node].update(children)
        for child in children:
            self._parents[child].add(node)

