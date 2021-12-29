#!/usr/bin/env python3

generator_buses = {
    '611',
    '671',
}



# Per Xiaochu, polynomial written in increasing power
def gas_gen_cost(watts, a, b, c):
    cost = a + b*watts + c*watts**2
    return cost


generator_costs = {
    #----------------------------------------------------------------------
    # Specify generator cost functions in the following format
    # Bus: callable
    #
    # Unspecified buses do not have generators
    #----------------------------------------------------------------------
    '611': lambda watts: gas_gen_cost(watts, 0.1, 0.02, 0.003),
    '671': lambda watts: gas_gen_cost(watts, 0.2, 0.09, 0.001),
}
