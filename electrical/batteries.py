#!/usr/bin/env python3
buses = {
    '684',
    '692',
}

s_lims = {
    # bus: volt_amps
    '684': 1E6,
    '692': 1E6,
}

soc_lims = {
    # bus: (watt_hours_lo, watt_hours_hi)
    '684': (1, 10E6),
    '692': (1, 10E6),
}

soc_lims_lo = dict()
soc_lims_hi = dict()
for bus, (lo, hi) in soc_lims.items():
    soc_lims_lo[bus] = lo
    soc_lims_hi[bus] = hi

initial_soc = {
    # bus: watt_hours
    '684': 1,
    '692': 1,
}

inverter_efficiencies = {
    # bus: 0_to_1
    '684': 0.98,
    '692': 0.98,
}

charger_efficiencies = {
    # bus: 0_to_1
    '684': 0.95,
    '692': 0.95,
}
