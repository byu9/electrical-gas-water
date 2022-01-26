#!/usr/bin/env python3
from math import inf
pres_lims = {
    # node: (ft_lo, ft_hi)
    '1': (50, inf),
    '2': (50, inf),
    '3': (50, inf),
    '4': (50, inf),
    '5': (50, inf),
    '6': (50, inf),
    '7': (50, inf),
    '8': (50, inf),
}

pres_lims_lo = dict()
pres_lims_hi = dict()
for node, (lo, hi) in pres_lims.items():
    pres_lims_lo[node] = lo
    pres_lims_hi[node] = hi



elevation = {
    # node: elevation_ft
    '1': 700,
    '2': 700,
    '3': 710,
    '4': 700,
    '5': 650,
    '6': 700,
    '7': 700,
    '8': 830,
}

reference_elevation = 700

elevation_induced_pressure = {
    node: reference_elevation - node_elevation
    for node, node_elevation in elevation.items()
}
