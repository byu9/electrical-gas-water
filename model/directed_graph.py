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
        
    def add_parent(self, node, parents):
        parents = set(parents)
        
        if node not in self._nodes:
            raise ValueError('Adding parents of a nonexistent node.')

        for parent in parents:
            if parent not in self._nodes:
                raise ValueError('Nonexistent parent.')

        self._parents[node].update(parents)
        for parent in parents:
            self._children[parent].add(node)

