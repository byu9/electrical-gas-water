#!/usr/bin/env python3

nodes = {
    'N05',
}
storage_efficiency = 0.95


initial_soc = {
    # node: mcf
    'N05': 1,
}



charging_flow_lims = {
    # node: mcf_per_h
    'N05': 100,
}

discharge_flow_lims = {
    # node: mcf_per_h
    'N05': 100,
}



soc_lims = {
    # node: (mcf_lo, mcf_hi)
    'N05': (2, 500),
}

soc_lims_lo = dict()
soc_lims_hi = dict()
for node, (lo, hi) in soc_lims.items():
    soc_lims_lo[node] = lo
    soc_lims_hi[node] = hi
