#!/usr/bin/env python3
from directed_graph import DirectedGraph

# The dataset does not contain any direction information
# Creating it manually...
buses = {
    # bus: children
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
    # substation 650 as impedance from ideal source 0
    # '0': {'650'},
}

digraph = DirectedGraph(buses.keys())
for bus, children in buses.items():
    digraph.add_children(bus, children)

## Testing
# for node in digraph.nodes:
#     print('{} -> {}'.format(node, ', '.join(digraph.parents_of(node))))
#
# for node in digraph.nodes:
#     print('{} <- {}'.format(node, ', '.join(digraph.children_of(node))))



# use as key to index (i, j) and (j, i) the same way
class Line:
    def __init__(self, i, j):
        self.endpoints = frozenset({i, j})

    def __eq__(self, other):
        return isinstance(other, Line) and (self.endpoints == other.endpoints)

    def __hash__(self):
        return hash(self.endpoints)

    def __repr__(self):
        return 'Line {}'.format('-'.join(self.endpoints))



def feet_to_miles(feet):
    FEET_PER_MILE = 5280
    miles = feet / FEET_PER_MILE
    return miles



line_segments = {
    # Line(from_bus, to_bus): (line_type, length_in_miles)
    Line('632', '645'): ('603', feet_to_miles(500)),
    Line('632', '633'): ('602', feet_to_miles(500)),
    # transformer impedance to be stored as per-mile for convenience
    Line('633', '634'): ('XFM-1', 1),
    Line('645', '646'): ('603', feet_to_miles(300)),
    Line('650', '632'): ('601', feet_to_miles(2000)),
    Line('684', '652'): ('607', feet_to_miles(800)),
    Line('632', '671'): ('601', feet_to_miles(2000)),
    Line('671', '684'): ('604', feet_to_miles(300)),
    Line('671', '680'): ('601', feet_to_miles(1000)),
    # switch impedance to be stored as per-mile for convenience
    Line('671', '692'): ('Switch', 1),
    Line('684', '611'): ('605', feet_to_miles(300)),
    Line('692', '675'): ('606', feet_to_miles(500)),
    # substation impedance to be stored as per-mile for convenience
    # Line('0', '650'): ('Substation', 1),
}



def per_unit_to_ohms(pu, volt_amp, volt):
    ohms_base = volt**2 / volt_amp
    ohms = pu * ohms_base
    return ohms



# Per Xiaochu, assume single phase using phase C data
segment_z = {
    # line_type: ohms_per_mile
    '601': 0.3414 + 1.0348j,
    '602': 0.7436 + 1.2112j,
    '603': 1.3238 + 1.3569j,
    '604': 1.3294 + 1.3471j,
    '605': 1.3292 + 1.3475j,
    '606': 0.7982 + 0.4463j,
    # does not have C phase. A used instead.
    '607': 1.3425 + 0.5124j,

    # stored as per-mile for convenience
    # ohms at 4.16kV side
    # Per Junkai, normalizing to the primary side to avoid per-unit
    'XFM-1': per_unit_to_ohms(pu=(1.1+2j)/100,
                              volt_amp=500E3, volt=4.16E3),

    # stored as per-mile for convenience
    # Per Xiaochu, the switch is always closed
    'Switch': 0,

    # stored as per-mile for convenience
    # ohms at 4.16kV side
    'Substation': per_unit_to_ohms(pu=(1+8j)/100,
                                   volt_amp=5E6, volt=4.16E3),
}



# Per Xiaochu, assume single phase using phase C data
segment_b = {
    # line_type: siemens_per_mile
    '601': 5.6386E-3,
    '602': 5.4246E-3,
    '603': 4.6658E-3,
    '604': 4.7097E-3,
    '605': 4.5193E-3,
    '606': 96.8897E-3,
    # does not have C phase. A used instead.
    '607': 88.9912E-3,
    'XFM-1': 0,
    'Switch': 0,
    'Substation': 0,
}


line_z = {
    line: segment_z[seg_type] * miles
    for line, (seg_type, miles) in line_segments.items()
}

line_r = {line: z.real for line, z in line_z.items()}
line_x = {line: z.imag for line, z in line_z.items()}



