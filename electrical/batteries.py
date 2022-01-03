#!/usr/bin/env python3

battery_buses = {
    '684',
    '692',
}

battery_s_lims = {
    # bus: volt_amps
    '684': 1E6,
    '692': 1E6,
}

battery_charge_lims = {
    # bus: (watt_hours_lo, watt_hours_hi)
    '684': (1, 10E6),
    '692': (1, 10E6),
}


battery_charge_lims_lo = dict()
battery_charge_lims_hi = dict()

for bus, (lo, hi) in battery_charge_lims.items():
    battery_charge_lims_lo[bus] = lo
    battery_charge_lims_hi[bus] = hi


battery_initial_charge = {
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
