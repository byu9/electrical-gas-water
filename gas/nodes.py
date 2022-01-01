#!/usr/bin/env python3
from misc.unit_conversions import bar_to_psi

pressure_lims = {
    # node: (psi_lo, psi_hi)
    'entry01': (bar_to_psi(40), bar_to_psi(70)),
    'entry03': (bar_to_psi(40), bar_to_psi(70)),
    'entry02': (bar_to_psi(40), bar_to_psi(70)),
    'exit01':  (bar_to_psi(40), bar_to_psi(70)),
    'exit02':  (bar_to_psi(40), bar_to_psi(60)),
    'exit03':  (bar_to_psi(40), bar_to_psi(60)),
    'N01':     (bar_to_psi(40), bar_to_psi(70)),
    'N02':     (bar_to_psi(40), bar_to_psi(70)),
    'N03':     (bar_to_psi(40), bar_to_psi(70)),
    'N04':     (bar_to_psi(40), bar_to_psi(70)),
    'N05':     (bar_to_psi(40), bar_to_psi(70)),
}

# squared pressure limits
sq_pressure_lims_hi = dict()
sq_pressure_lims_lo = dict()
for node, (lo, hi) in pressure_lims.items():
    sq_pressure_lims_lo[node] = lo**2
    sq_pressure_lims_hi[node] = hi**2
