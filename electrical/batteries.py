#!/usr/bin/env python3

battery_buses = {
    '684',
    '692',
}

battery_s_lims = {
    '684': 1E6,
    '692': 1E6,
}

battery_charge_lims = {
    '684': (1, 10E6),
    '692': (1, 10E6),
}


battery_charge_lims_lo = dict()
battery_charge_lims_hi = dict()

for bus, (lo, hi) in battery_charge_lims.items():
    battery_charge_lims_lo[bus] = lo
    battery_charge_lims_hi[bus] = hi


battery_initial_charge = {
    '684': 1,
    '692': 1,
}

inverter_efficiencies = {
    #----------------------------------------------------------------------
    # Specify inverters in the following format
    # bus: efficiency
    #
    # Unspecified buses do not have inverters
    #----------------------------------------------------------------------
    '684': 0.98,
    '692': 0.98,
}

charger_efficiencies = {
    #----------------------------------------------------------------------
    # Specify chargers in the following format
    # bus: efficiency
    #
    # Unspecified buses do not have chargers
    #----------------------------------------------------------------------
    '684': 0.95,
    '692': 0.95,
}
