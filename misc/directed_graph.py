#!/usr/bin/env python3
class DirectedGraph:
    _parents = dict()
    _children = dict()

    def __init__(self, nodes):
        nodes = set(nodes)
        for node in nodes:
            self._children[node] = set()
            self._parents[node] = set()

    def add_children(self, node, children):
        """
        Adds directional edges from a node to its children
        """
        children = set(children)
        self._children[node].update(children)
        for child in children:
            self._parents[child].add(node)

    @property
    def nodes(self):
        return self._children.keys()

    @property
    def edges(self):
        for node in self.nodes:
            for child in self._children[node]:
                yield (node, child)

    def __repr__(self):
        edges = ', '.join('{}->{}'.format(*edge) for edge in self.edges)
        nodes = ', '.join(self.nodes)

        return 'Directed graph\nNodes\n{}\n\nEdges\n{}\n'.format(
            nodes, edges)

    #----------------------------------------------------------------------
    # Returns direct relatives
    #----------------------------------------------------------------------
    def parents_of(self, node):
        yield from self._parents[node]

    def children_of(self, node):
        yield from self._children[node]

    #----------------------------------------------------------------------
    # Returns direct and indirect relatives
    #----------------------------------------------------------------------
    def descendents_of(self, node):
        children = self._children[node]

        yield from children

        for child in children:
            yield from self.descendents_of(child)

    def ancestors_of(self, node):
        parents = self._parents[node]

        yield from parents

        for parent in parents:
            yield from self.ancestors_of(parent)
