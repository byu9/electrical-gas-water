#!/usr/bin/env python3
from misc.directed_graph import DirectedGraph

children = {
    'entry01': {'entry03'},
    'entry02': {'N03'},
    'entry03': {'N01'},

    'exit01': {},
    'exit02': {},
    'exit03': {},

    'N01': {'N02', 'N03'},
    'N02': {'exit01', 'N04'},
    'N03': {'N04'},
    'N04': {'N05'},
    'N05': {'exit02', 'exit03'},
}

graph = DirectedGraph(children.keys())
for node, children in children.items():
    graph.add_children(node, children)
