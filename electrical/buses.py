#!/usr/bin/env python3

bus_v_lims = {
    # bus: (volts_lo, volts_hi)
    # Per Junkai, using 0.95~1.05
    '650': (0.95*4.16E3, 1.05*4.16E3),
    '632': (0.95*4.16E3, 1.05*4.16E3),
    '645': (0.95*4.16E3, 1.05*4.16E3),
    '646': (0.95*4.16E3, 1.05*4.16E3),
    '633': (0.95*4.16E3, 1.05*4.16E3),
    '634': (0.95*4.16E3, 1.05*4.16E3),
    '671': (0.95*4.16E3, 1.05*4.16E3),
    '684': (0.95*4.16E3, 1.05*4.16E3),
    '611': (0.95*4.16E3, 1.05*4.16E3),
    '652': (0.95*4.16E3, 1.05*4.16E3),
    '680': (0.95*4.16E3, 1.05*4.16E3),
    '692': (0.95*4.16E3, 1.05*4.16E3),
    '675': (0.95*4.16E3, 1.05*4.16E3),
    # normalized to 4.16kV side
    'Grid':(0.95*4.16E3, 1.05*4.16E3),
}

bus_v_lims_lo = dict()
bus_v_lims_hi = dict()

for bus, lims in bus_v_lims.items():
    lo, hi = lims

    bus_v_lims_lo[bus] = lo
    bus_v_lims_hi[bus] = hi
