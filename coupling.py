#!/usr/bin/env python3
from math import inf

# Per Xiaochu, polynomial written in increasing power
def coal_gen_cost(watts, a, b, c):
    mega_watts = watts / 1E6
    dollars_per_hour = a + b * mega_watts + c * mega_watts**2
    return dollars_per_hour

def gas_gen_cost(watts):
    # Per Xiaochu, gas generator costs counted by gas demand and not here
    dollars_per_hour = 0
    return dollars_per_hour

def wholesale_elec_cost(watts, dollars_per_mega_watt_hour):
    mega_watts = watts / 1E6
    dollars_per_hour = mega_watts * dollars_per_mega_watt_hour
    return dollars_per_hour

generator_cost_funcs = {
    # bus: callable(watts) -> dollars_per_hour
    'Grid': lambda watts, t: wholesale_elec_cost(watts, 13.5),
    '632': lambda watts, t: coal_gen_cost(watts, 40, 11, 0.5),
    '671': lambda watts, t: gas_gen_cost(watts),
}
generator_buses = generator_cost_funcs.keys()

#----------------------------------------------------------------------
gas_generator_mappings = {
    # elec_bus: gas_node,
    '671': 'exit03',
}
gas_generator_buses = set(gas_generator_mappings.keys())
gas_generator_nodes = set(gas_generator_mappings.values())
gas_generator_efficiency = 0.95

gas_generator_flow_lims = {
    # node: (mcf_per_h_lo, mcf_per_h_hi)
    'N02': (0, +inf),
    'exit03': (0, +inf),
}
gas_generator_flow_lims_lo = dict()
gas_generator_flow_lims_hi = dict()
for node, (lo, hi) in gas_generator_flow_lims.items():
    gas_generator_flow_lims_lo[node] = lo
    gas_generator_flow_lims_hi[node] = hi



power_to_gas_mappings = {
    # elec_bus: gas_node
    '632': 'N02',
}
power_to_gas_buses = set(power_to_gas_mappings.keys())
power_to_gas_nodes = set(power_to_gas_mappings.values())
power_to_gas_efficiency = 0.95

# in watt-hours-per-thousand-cubic-feet (Wh/MCF)
natural_gas_heat_value = 302.33E3


#----------------------------------------------------------------------
generator_p_lims = {
    # bus: (watts_lo, watts_hi)
    'Grid': (0, +inf),
    '632': (1E6, 5E6),
    '671': (1E6, 5E6),
}
generator_p_lims_lo = dict()
generator_p_lims_hi = dict()
for bus, (lo, hi) in generator_p_lims.items():
    generator_p_lims_lo[bus] = lo
    generator_p_lims_hi[bus] = hi


generator_q_lims = {
    # bus: (vars_lo, vars_hi)
    'Grid': (-inf, +inf),
    '632': (-inf, +inf),
    '671': (-inf, +inf),
}
generator_q_lims_lo = dict()
generator_q_lims_hi = dict()
for bus, (lo, hi) in generator_q_lims.items():
    generator_q_lims_lo[bus] = lo
    generator_q_lims_hi[bus] = hi


#----------------------------------------------------------------------
power_to_gas_p_lims = {
    # bus: (watts_lo, watts_hi)
    '632': (0, inf),
}
power_to_gas_p_lims_lo = dict()
power_to_gas_p_lims_hi = dict()
for bus, (lo, hi) in power_to_gas_p_lims.items():
    power_to_gas_p_lims_lo[bus] = lo
    power_to_gas_p_lims_hi[bus] = hi

power_to_gas_q_lims = {
    # bus: (watts_lo, watts_hi)
    '632': (0, inf),
}
power_to_gas_q_lims_lo = dict()
power_to_gas_q_lims_hi = dict()
for bus, (lo, hi) in power_to_gas_q_lims.items():
    power_to_gas_q_lims_lo[bus] = lo
    power_to_gas_q_lims_hi[bus] = hi

power_to_gas_output_lims = {
    # in thousand-cubic-feet-per-hour (MCF/h)
    # node: (lo, hi)
    'N02': (0, inf),
}
power_to_gas_output_lims_lo = dict()
power_to_gas_output_lims_hi = dict()
for bus, (lo, hi) in power_to_gas_output_lims.items():
    power_to_gas_output_lims_lo[bus] = lo
    power_to_gas_output_lims_hi[bus] = hi


#----------------------------------------------------------------------
water_pump_buses = {}
water_pump_p_lims_lo = dict()
water_pump_p_lims_hi = dict()
water_pump_q_lims_lo = dict()
water_pump_q_lims_hi = dict()
