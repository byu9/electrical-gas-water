#!/usr/bin/env python3
from misc.unit_conversions import mcmph_to_mcfph

nodes = {
    'entry01',
    'entry02',
    'entry03',
}

lims = {
    # 'node': (mcf_per_hour_lo, mcf_per_hour_hi)
    'entry01' : (mcmph_to_mcfph(50)  , mcmph_to_mcfph(750)),
    'entry02' : (mcmph_to_mcfph(100) , mcmph_to_mcfph(500)),
    'entry03' : (mcmph_to_mcfph(0)   , mcmph_to_mcfph(500)),
}

lims_hi = dict()
lims_lo = dict()
for node, (lo, hi) in lims.items():
    lims_hi[node] = hi
    lims_lo[node] = lo

costs = {
    # (node, time): dollars_per_mcf
    ('entry01', '2022-01-01T00:00:00Z'): 0.14,
    ('entry02', '2022-01-01T00:00:00Z'): 0.15,
    ('entry03', '2022-01-01T00:00:00Z'): 0.16,

    ('entry01', '2022-01-01T00:01:00Z'): 0.145,
    ('entry02', '2022-01-01T00:01:00Z'): 0.155,
    ('entry03', '2022-01-01T00:01:00Z'): 0.165,
}

cost_funcs = {
    # node: callable(mcf_per_hour) -> dollars_per_hour
    m: lambda mcf_per_hour, t: mcf_per_hour * costs[m,t]

    for m in nodes
}
