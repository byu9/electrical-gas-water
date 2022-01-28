#!/usr/bin/env python3
from math import sqrt
from optimize import (
    T,
    G_elec, G_gas, G_water,

    v, PG, QG, PP, QP, PES, QES, PT, QT, P, Q, l, LES, EES,
    generator_buses,
    water_pump_buses,
    battery_buses,
    power_to_gas_buses,

    Pi, GLS, GT, GLch, GLdis, GLG, tau, GL, SOC,
    gas_supply_nodes,
    gas_storage_nodes,
    gas_generator_nodes,
    compressor_lines,

    y, fG, fT, f, alpha, SW,
    water_supply_nodes,
    water_storage_nodes,
    water_pump_lines,

    model
)

import gurobipy as gurobi


def get_val(v):
    return v.X if isinstance(v, gurobi.Var) else v


print('#'*70 + '\n# results\n' + '#'*70)
pretty = dict()


pretty = [
    (
        'Voltage on {:>4}, t={:>20}'.format(i,t),
        '{:>6.3f} kV'.format(sqrt(v[i,t].X)/1000)
    )

    for i in G_elec.nodes
    for t in T
]

pretty += [
    (
        'Generator output on {:>4}, t={:>20}'.format(i, t),
        '{:>6.3f} MW, {:>6.3f} MVar'.format(get_val(PG[i,t])/1E6,
                                            get_val(QG[i,t])/1E6)
    )

    for i in generator_buses
    for t in T
]

pretty += [
    (
        'Water pump power on {:>4}, t={:>20}'.format(i, t),
        '{:>6.3f} MW, {:>6.3f} MVar'.format(get_val(PP[i,t])/1E6,
                                            get_val(QP[i,t])/1E6)
    )

    for i in water_pump_buses
    for t in T
]

pretty += [
    (
        'Battery discharge on {:>4}, t={:>20}'.format(i, t),
        '{:>6.3f} MW, {:6.3f} MVar'.format(get_val(PES[i,t])/1E6,
                                           get_val(QES[i,t])/1E6)
    )

    for i in battery_buses
    for t in T
]

pretty += [
    (
        'Power to gas on {:>4}, t={:>20}'.format(i, t),
        '{:6.3f} MW, {:6.3f} MVar'.format(get_val(PES[i,t])/1E6,
                                          get_val(QES[i,t])/1E6)

    )

    for i in power_to_gas_buses
    for t in T
]

pretty += [
    (
        'Power over {:>4} --> {:>4}, t={:>20}'.format(i,j,t),
        '{:6.3f} MW, {:6.3f} MVar'.format(get_val(P[i,j,t])/1E6,
                                          get_val(Q[i,j,t])/1E6)
    )

    for (i, j) in G_elec.edges
    for t in T
]

pretty += [
    (
        'Current over {:>4} --> {:>4}, t={:>20}'.format(i,j,t),
        '{:6.3f} kA'.format(sqrt(get_val(l[i,j,t])/1E3))
    )

    for (i, j) in G_elec.edges
    for t in T
]

pretty += [
    (
        'Battery state of charge on {:>4}, t={:>20}'.format(i,t),
        '{:6.3f} MWh'.format(get_val(EES[i,t])/1E6)
    )

    for i in battery_buses
    for t in T
]

pretty += [
    (
        'Battery power loss on {:>4}, t={:>20}'.format(i,t),
        '{:6.3f} MW'.format(get_val(LES[i,t])/1E6)
    )

    for i in battery_buses
    for t in T
]

pretty += [
    (
        'Gas pressure on {:>8}, t={:>20}'.format(m, t),
        '{:6.3f} PSI'.format(sqrt(get_val(Pi[m,t])))
    )
    for m in G_gas.nodes
    for t in T
]

pretty += [
    (
        'Gas supply on {:>8}, t={:>20}'.format(m, t),
        '{:8.3f} MCF/h'.format(get_val(GLS[m,t]))
    )
    for m in gas_supply_nodes
    for t in T
]

pretty += [
    (
        'Gas storage on {:>8}, t={:>20}'.format(m, t),
        'ch {:8.3f} MCF/h, dis {:8.3f} MCF/h'.format(get_val(GLch[m,t]),
                                                     get_val(GLdis[m,t]))
    )
    for m in gas_storage_nodes
    for t in T
]

pretty += [
    (
        'Gas generator on {:>8}, t={:20}'.format(m, t),
        '{:8.3f} MCF/h'.format(get_val(GLG[m,t]))
    )

    for m in gas_generator_nodes
    for t in T
]

pretty += [
    (
        'Compressor consumption on {:>8}, t={:20}'.format(s, t),
        '{:8.3f} MCF/h'.format(get_val(tau[s, t]))
    )

    for (s, _) in compressor_lines
    for t in T
]


pretty += [
    (
        'Gas flow over {:>8} --> {:>8}, t={:20}'.format(s, r, t),
        '{:8.3f} MCF/h'.format(get_val(GL[s,r,t]))
    )

    for (s, r) in G_gas.edges
    for t in T
]

pretty += [
    (
        'Gas storage state of charge on {:>8}, t={:20}'.format(m, t),
        '{:8.3f} MCF'.format(get_val(SOC[m,t]))
    )

    for m in gas_storage_nodes
    for t in T
]


pretty += [
    (
        'Water pressure on {:>3}, t={:>20}'.format(k, t),
        '{:>6.3f} Ft_W'.format(get_val(y[k, t]))
    )
    for k in G_water.nodes
    for t in T
]

pretty += [
    (
        'Water supply on {:>3}, t={:>20}'.format(k, t),
        '{:>6.3f} Gal/h'.format(get_val(fG[k, t]))
    )
    for k in water_supply_nodes
    for t in T
]


pretty += [
    (
        'Water storage flow on {:>3}, t={:>20}'.format(k, t),
        '{:>6.3f} Gal/h'.format(get_val(fT[k, t]))
    )
    for k in water_storage_nodes
    for t in T
]


pretty += [
    (
        'Water flow over {:>3} --> {:>3}, t={:>20}'.format(k, n, t),
        '{:>6.3f} Gal/h'.format(get_val(f[k,n,t]))
    )

    for (k, n) in G_water.edges
    for t in T
]

pretty += [
    (
        'Status of pump on {:>3}, t={:>20}'.format(k, t),
        '{:>5}'.format('on' if get_val(alpha[k,n,t]) else 'off')
    )
    for (k, n) in water_pump_lines
    for t in T
]

pretty += [
    (
        'Water storage state of charge on {:>3}, t={:>20}'.format(k,t),
        '{:>8.3f} Gal'.format(get_val(SW[k,t]))
    )
    for k in water_storage_nodes
    for t in T
]

pretty += [
    (
        'Objective',
        '{:>8.3f} USD'.format(model.objVal)
    )

]

print('\n'.join([
    '{}: {}'.format(*v)
    for v in pretty
]))
