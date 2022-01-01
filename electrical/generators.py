#!/usr/bin/env python3
from math import inf


generator_buses = {
    '632',
    '671',
    '650',
}



# Per Xiaochu, polynomial written in increasing power
# watts -> MW since a, b, c are based on $/MWh
def gas_gen_cost(watts, a, b, c):
    mega_watts = watts / 1E6
    dollars = a + b * mega_watts + c * mega_watts**2
    return dollars

def coal_gen_cost(watts, a, b, c):
    mega_watts = watts / 1E6
    dollars = a + b * mega_watts + c * mega_watts**2
    return dollars


def wholesale_cost(watts, dollars_per_mega_watt):
    mega_watts = watts / 1E6
    dollars = mega_watts * dollars_per_mega_watt
    return dollars



generator_costs = {
    #----------------------------------------------------------------------
    # Specify generator cost functions in the following format
    # Bus: callable
    #
    # Unspecified buses do not have generators
    #----------------------------------------------------------------------
    '632': lambda watts: coal_gen_cost(watts, 40, 11, 0.5),
    '671': lambda watts: gas_gen_cost(watts, 20, 9, 1),
    '650': lambda watts: wholesale_cost(watts, 13.5),
}

generator_p_lims = {
    '632': (1E6, 5E6),
    '671': (0.5E6, 2E6),
    '650': (0, +inf),
}

generator_q_lims = {
    '632': (0, +inf),
    '671': (0, +inf),
    '650': (0, +inf),
}

generator_p_lims_lo = dict()
generator_p_lims_hi = dict()
generator_q_lims_lo = dict()
generator_q_lims_hi = dict()

for bus in generator_buses:
    p_lo, p_hi = generator_p_lims[bus]
    q_lo, q_hi = generator_q_lims[bus]

    generator_p_lims_lo[bus] = p_lo
    generator_p_lims_hi[bus] = p_hi
    generator_q_lims_lo[bus] = q_lo
    generator_q_lims_hi[bus] = q_hi
