#!/usr/bin/env python3
import gurobipy as gurobi

from misc.directed_graph import (
    DirectedGraph,
)

from timeseries.scheduling_horizon import (
    scheduling_horizon as T,
)

from electrical.topology import (
    children as bus_children,
)

from electrical.buses import (
    bus_v_lims_lo as vlims_lo,
    bus_v_lims_hi as vlims_hi,
)

from electrical.power_lines import (
    line_r as r,
    line_x as x,
    line_i_lims as ilims,
    line_s_lims as slims,
)

from electrical.loads import (
    p_loads as PL,
    q_loads as QL,
)

from electrical.renewables import (
    p_renewables as PR,
    q_renewables as QR,
    renewable_buses,
)

from electrical.batteries import (
    inverter_efficiencies as rcvt,
    charger_efficiencies as rbatt,
    battery_buses,
    battery_s_lims as SESlims,
    battery_charge_lims_lo as EESlims_lo,
    battery_charge_lims_hi as EESlims_hi,
    battery_initial_charge as EES0,
)

from electrical.generators import (
    generator_costs as Cp,
    generator_buses,
    generator_p_lims_lo as PGlims_lo,
    generator_p_lims_hi as PGlims_hi,
    generator_q_lims_lo as QGlims_lo,
    generator_q_lims_hi as QGlims_hi,
)

from electrical.power_to_gas import (
    power_to_gas_buses,
)

from electrical.water_pumps import (
    water_pump_buses,
)

#----------------------------------------------------------------------
# Creates topology graph
#----------------------------------------------------------------------
G = DirectedGraph(bus_children.keys())
for bus, children in bus_children.items():
    G.add_children(bus, children)

# Converts generators to sets, so it can be repeatedly iterated
buses = set(G.descendents_of('Grid'))
lines = set(G.edges)


model = gurobi.Model()
#----------------------------------------------------------------------
# Decision variables for power lines
#----------------------------------------------------------------------
P = {
    (i, j, t): model.addVar(name='P({}->{})@{}'.format(i, j, t))

    for (i, j) in lines
    for t in T
}

Q = {
    (i, j, t): model.addVar(name='Q({}->{})@{}'.format(i, j, t))

    for (i, j) in lines
    for t in T
}

l = {
    (i, j, t): model.addVar(name='l({}->{})@{}'.format(i, j, t),
                            lb=0,
                            ub=ilims[i,j]**2)

    for (i, j) in lines
    for t in T
}


#----------------------------------------------------------------------
# Decision variables for buses
#----------------------------------------------------------------------
PG = {
    (i, t): model.addVar(name='PG({})@{}'.format(i, t),
                         lb=PGlims_lo[i],
                         ub=PGlims_hi[i])

    for i in generator_buses
    for t in T
}

QG = {
    (i, t): model.addVar(name='QG({})@{}'.format(i, t),
                         lb=QGlims_lo[i],
                         ub=QGlims_hi[i])

    for i in generator_buses
    for t in T
}

Pch = {
    (i, t): model.addVar(name='Pch({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}

Qch = {
    (i, t): model.addVar(name='Qch({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}


Pdis = {
    (i, t): model.addVar(name='Pdis({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}

Qdis = {
    (i, t): model.addVar(name='Qdis({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}

PT = {
    (i, t): model.addVar(name='PT({})@{}'.format(i, t))

    for i in power_to_gas_buses
    for t in T
}

QT = {
    (i, t): model.addVar(name='QT({})@{}'.format(i, t))

    for i in power_to_gas_buses
    for t in T
}


PP = {
    (i, t): model.addVar(name='PP({})@{}'.format(i, t))

    for i in water_pump_buses
    for t in T
}

QP = {
    (i, t): model.addVar(name='QP({})@{}'.format(i, t))

    for i in water_pump_buses
    for t in T
}

v = {
    (i, t): model.addVar(name='v({})@{}'.format(i, t),
                         lb=vlims_lo[i]**2,
                         ub=vlims_hi[i]**2)

    for i in buses
    for t in T
}


PES = {
    (i, t): model.addVar(name='PES({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}

QES = {
    (i, t): model.addVar(name='QES({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}


LES = {
    (i, t): model.addVar(name='LES({})@{}'.format(i, t))

    for i in battery_buses
    for t in T
}

#----------------------------------------------------------------------
# Creates objective
#----------------------------------------------------------------------
model.setObjective(sum(
    sum(Cp[i](PG[i,t]) for i in generator_buses)

    for t in T
), gurobi.GRB.MINIMIZE)


#----------------------------------------------------------------------
# Creates constraints
#----------------------------------------------------------------------
model.addConstrs((
    sum(P[i,j,t]                     for j in G.children_of(i)) -
    sum(P[k,i,t] - r[k,i] * l[k,i,t] for k in G.parents_of(i))

    ==

    (PG   [i,t] if i in generator_buses    else 0) +
    (PR   [i,t] if i in renewable_buses    else 0) +
    (Pdis [i,t] if i in battery_buses      else 0) -
    (PT   [i,t] if i in power_to_gas_buses else 0) -
    (PL   [i,t]                                  ) -
    (PP   [i,t] if i in water_pump_buses   else 0) -
    (Pch  [i,t] if i in battery_buses      else 0)

    for i in buses
    for t in T
), name='1a')

model.addConstrs((
    sum(Q[i,j,t]                     for j in G.children_of(i)) -
    sum(Q[k,i,t] - x[k,i] * l[k,i,t] for k in G.parents_of(i))

    ==

    (QG   [i,t] if i in generator_buses    else 0) +
    (QR   [i,t] if i in renewable_buses    else 0) +
    (Qdis [i,t] if i in battery_buses      else 0) -
    (QT   [i,t] if i in power_to_gas_buses else 0) -
    (QL   [i,t]                                  ) -
    (QP   [i,t] if i in water_pump_buses   else 0) -
    (Qch  [i,t] if i in battery_buses      else 0)

    for i in buses
    for t in T
), name='1b')

model.addConstrs((
    v[i,t] - v[j,t]

    ==

    2 * r[i,j] * P[i,j,t] +
    2 * x[i,j] * Q[i,j,t] -
    (r[i,j]**2 + x[i,j]**2) * l[i,j,t]

    for i in buses
    for j in G.children_of(i)
    for t in T
), name='1c')

# Per Xiaochu, constraint 1d converted to 1e-1f
model.addConstrs((
    P[i,j,t]**2 + Q[i,j,t]**2

    <=

    v[i,t] * l[i,j,t]

    for i in buses
    for j in G.children_of(i)
    for t in T
), name='1e')

# Per Xiaochu constraint 1d converted to 1e-1f
model.addConstrs((
    slims[i,j]**2 * v[i,t] + vlims_lo[i]**2 * vlims_hi[i]**2 * l[i,j,t]

    <=

    slims[i,j]**2 * (vlims_lo[i]**2 + vlims_hi[i]**2)

    for i in buses
    for j in G.children_of(i)
    for t in T
), name='1f')

model.addConstrs((
    P[i,j,t]**2 + Q[i,j,t]**2

    <=

    slims[i,j]**2

    for i, j in lines
    for t in T
), name='1g')

# 1h - 1i added as decision variable attribute



model.addConstrs((
    (rbatt[i] + rcvt[i]) * PES[i,t]**2 + rcvt[i] * QES[i,t]**2

    <=

    LES[i,t] * v[i,t]

    for i in battery_buses
    for t in T
), name='2b')

model.addConstrs((
    rbatt[i] * QES[i,t]**2 + vlims_lo[i]**2 * LES[i,t]

    <=

    SESlims[i]**2 * (rbatt[i] + rcvt[i])

    for i in battery_buses
    for t in T
), name='2c')

model.addConstrs((
    SESlims[i]**2 * v[i,t] + vlims_lo[i]**2 * vlims_hi[i]**2 * LES[i,t]

    <=

    SESlims[i]**2 * (vlims_lo[i]**2 + vlims_hi[i]**2)

    for i in battery_buses
    for t in T
), name='2d')

model.addConstrs((
    PES[i,t]**2 + QES[i,t]**2

    <=

    SESlims[i]**2

    for i in battery_buses
    for t in T
), name='2e')


for i in battery_buses:
    expr = EES0[i] - sum(PES[i,t] + LES[i,t] for t in T)

    model.addConstr(EESlims_lo[i] <= expr, name='2f')
    model.addConstr(expr <= EESlims_hi[i], name='2f')


model.optimize()
model.display()
