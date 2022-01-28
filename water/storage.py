#!/usr/bin/env python3
from misc.unit_conversions import gpm_to_gph

nodes = {
    '8',
}

storage_flow_lims = {
    # node: (gal_per_h_lo, gal_per_h_hi),
    '8': (gpm_to_gph(-6000), gpm_to_gph(6000)),
}

storage_flow_lims_lo = dict()
storage_flow_lims_hi = dict()
for node, (lo, hi) in storage_flow_lims.items():
    storage_flow_lims_lo[node] = lo
    storage_flow_lims_hi[node] = hi




initial_soc = {
    # node, gallons
    '8': 2,
}

soc_lims = {
    # node: (gal_lo, gal_hi),
    '8': (0, 6000),
}

soc_lims_lo = dict()
soc_lims_hi = dict()
for node, (lo, hi) in soc_lims.items():
    soc_lims_lo[node] = lo
    soc_lims_hi[node] = hi
