#!/usr/bin/env python3

battery_buses = {
    '675',
    '671',
}

battery_s_lims = {
    '675': 1E6,
    '671': 1E6,
}

battery_charge_lims = {
    '675': (1, 10E6),
    '671': (1, 10E6),
}


battery_charge_lims_lo = dict()
battery_charge_lims_hi = dict()

for bus, (lo, hi) in battery_charge_lims.items():
    battery_charge_lims_lo[bus] = lo
    battery_charge_lims_hi[bus] = hi


battery_initial_charge = {
    '675': 1,
    '671': 1,
}

inverter_efficiencies = {
    #----------------------------------------------------------------------
    # Specify inverters in the following format
    # bus: efficiency
    #
    # Unspecified buses do not have inverters
    #----------------------------------------------------------------------
    '675': 0.98,
    '671': 0.98,
}

charger_efficiencies = {
    #----------------------------------------------------------------------
    # Specify chargers in the following format
    # bus: efficiency
    #
    # Unspecified buses do not have chargers
    #----------------------------------------------------------------------
    '675': 0.95,
    '671': 0.95,
}
