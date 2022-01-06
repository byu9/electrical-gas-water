#!/usr/bin/env python3
from misc.directed_graph import DirectedGraph

children = {
    # bus: {children, ...}
    '650': {'632'},
    '632': {'645', '671', '633'},
    '645': {'646'},
    '646': {},
    '633': {'634'},
    '634': {},
    '671': {'684', '680', '692'},
    '684': {'611', '652'},
    '611': {},
    '652': {},
    '680': {},
    '692': {'675'},
    '675': {},
    # substation 650 as child of grid
    'Grid': {'650'},
}

graph = DirectedGraph(children.keys())
for bus, children in children.items():
    graph.add_children(bus, children)
