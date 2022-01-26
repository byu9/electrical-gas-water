#!/usr/bin/env python3
from misc.directed_graph import DirectedGraph

children = {
    # node: {children, ...}
    '1': {'2'},
    '2': {'3'},
    '3': {'4', '7'},
    '4': {'5', '6'},
    '5': {'6'},
    '6': {'7'},
    '7': {'8'},
    '8': {},
}

graph = DirectedGraph(children.keys())
for node, children in children.items():
    graph.add_children(node, children)
