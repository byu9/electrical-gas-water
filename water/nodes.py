#!/usr/bin/env python3

pres_lims = {
    # node: (ft_lo, ft_hi)
    '1': (10, 900),
    '2': (10, 900),
    '3': (10, 900),
    '4': (10, 900),
    '5': (10, 900),
    '6': (10, 900),
    '7': (10, 900),
    '8': (10, 900),
}

pres_lims_lo = dict()
pres_lims_hi = dict()
for node, (lo, hi) in pres_lims.items():
    pres_lims_lo[node] = lo
    pres_lims_hi[node] = hi



elevation = {
    # node: elevation_ft
    '1': 600,
    '2': 520,
    '3': 500,
    '4': 500,
    '5': 500,
    '6': 500,
    '7': 550,
    '8': 550,
}

reference_elevation = 0

elevation_induced_pressure = {
    node: reference_elevation - node_elevation
    for node, node_elevation in elevation.items()
}
