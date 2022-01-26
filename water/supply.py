#!/usr/bin/env python3

nodes = {
    '1',
}

flow_lims = {
    # node: (gal_per_h_lo, gal_per_h_hi)
    '1': (0, 5000),
}


flow_lims_lo = dict()
flow_lims_hi = dict()
for node, (lo, hi) in flow_lims.items():
    flow_lims_lo[node] = lo
    flow_lims_hi[node] = hi
