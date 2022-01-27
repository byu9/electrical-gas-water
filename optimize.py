#!/usr/bin/env python3
import gurobipy as gurobi
from math import inf

#----------------------------------------------------------------------
from timeseries import (
    scheduling_horizon as T,
    extended_scheduling_horizon as T_ext,
    extended_initial_timepoint as t0,
)

#----------------------------------------------------------------------
from electrical.topology import (
    graph as G_elec,
)

from electrical.buses import (
    sq_v_lims_lo,
    sq_v_lims_hi,
)

from electrical.lines import (
    r, x, z,
    sq_i_lims as l_lims,
    s_lims,
)

from electrical.batteries import (
    buses                 as battery_buses,
    initial_soc           as battery_initial_soc,
    soc_lims_lo           as EES_lims_lo,
    soc_lims_hi           as EES_lims_hi,
    s_lims                as SES_lims,
    charger_efficiencies  as rbatt,
    inverter_efficiencies as rcvt,
)

from electrical.renewables import (
    buses as renewable_buses,
    p as renewable_p,
    q as renewable_q,
)

from electrical.loads import (
    p as PL,
    q as QL,
)

#----------------------------------------------------------------------
from gas.topology import (
    graph as G_gas,
)

from gas.nodes import (
    sq_pressure_lims_lo as Pi_lims_lo,
    sq_pressure_lims_hi as Pi_lims_hi,
)

from gas.lines import (
    compressor_lines,
    compressor_line_source_nodes,
    flow_funcs as Phi,
    flow_lims_lo as GL_lims_lo,
    flow_lims_hi as GL_lims_hi,
)

from gas.supply import (
    nodes as gas_supply_nodes,
    cost_funcs as Cg,
    lims_lo as GLS_lims_lo,
    lims_hi as GLS_lims_hi,
)

from gas.demand import (
    gas_demands as Dgas,
)

from gas.storage import (
    nodes as gas_storage_nodes,
    storage_efficiency as eta_G,
    initial_soc as gas_storage_initial_soc,
    soc_lims_hi as SOC_lims_hi,
    soc_lims_lo as SOC_lims_lo,
    charging_flow_lims as GLch_lims,
    discharge_flow_lims as GLdis_lims,
)

#----------------------------------------------------------------------
from water.topology import (
    graph as G_water,
)

from water.nodes import (
    pres_lims_lo as y_lims_lo,
    pres_lims_hi as y_lims_hi,
    elevation_induced_pressure as h,
)

from water.lines import (
    water_pump_lines,
    pump_induced_pres_funcs as Phi_W,
    flow_lims_lo as f_lims_lo,
    flow_lims_hi as f_lims_hi,
    pres_loss_coeffs as RP,
)

from water.supply import (
    nodes as water_supply_nodes,
    flow_lims_lo as fG_lims_lo,
    flow_lims_hi as fG_lims_hi,
)

from water.demand import (
    demand as dW,
)

from water.storage import (
    nodes as water_storage_nodes,
    soc_lims_lo as SW_lims_lo,
    soc_lims_hi as SW_lims_hi,
    initial_soc as water_storage_initial_soc,
    storage_flow_lims_lo as fT_lims_lo,
    storage_flow_lims_hi as fT_lims_hi,
)



#----------------------------------------------------------------------
from coupling import (
    generator_buses,
    generator_cost_funcs         as Ce,
    generator_p_lims_lo          as PG_lims_lo,
    generator_p_lims_hi          as PG_lims_hi,
    generator_q_lims_lo          as QG_lims_lo,
    generator_q_lims_hi          as QG_lims_hi,

    gas_generator_buses,
    gas_generator_nodes,
    gas_generator_mappings,
    gas_generator_efficiency     as eta_G2P,
    gas_generator_flow_lims_lo   as GLG_lims_lo,
    gas_generator_flow_lims_hi   as GLG_lims_hi,

    power_to_gas_buses,
    power_to_gas_nodes,
    power_to_gas_mappings,
    power_to_gas_efficiency      as eta_P2G,
    power_to_gas_p_lims_lo       as PT_lims_lo,
    power_to_gas_p_lims_hi       as PT_lims_hi,
    power_to_gas_q_lims_lo       as QT_lims_lo,
    power_to_gas_q_lims_hi       as QT_lims_hi,
    power_to_gas_output_lims_lo  as GT_lims_lo,
    power_to_gas_output_lims_hi  as GT_lims_hi,

    natural_gas_heat_value       as HHVSNG,

    water_pump_buses,
    water_pump_mappings,
    water_pump_efficiencies      as eta_W,
    water_pump_p_lims_lo         as PP_lims_lo,
    water_pump_p_lims_hi         as PP_lims_hi,
    water_pump_q_lims_lo         as QP_lims_lo,
    water_pump_q_lims_hi         as QP_lims_hi,
)


#----------------------------------------------------------------------



model = gurobi.Model()

#----------------------------------------------------------------------
# For all electrical buses
#----------------------------------------------------------------------
v = {
    (i, t): model.addVar(name='v({})@{}'.format(i, t),
                         lb=sq_v_lims_lo[i],
                         ub=sq_v_lims_hi[i])

    for i in G_elec.nodes
    for t in T
}

PG = {
    (i, t): model.addVar(name='PG({})@{}'.format(i, t),
                         lb=PG_lims_lo[i],
                         ub=PG_lims_hi[i]) if i in generator_buses else 0

    for i in G_elec.nodes
    for t in T
}

QG = {
    (i, t): model.addVar(name='QG({})@{}'.format(i, t),
                         lb=QG_lims_lo[i],
                         ub=QG_lims_hi[i]) if i in generator_buses else 0

    for i in G_elec.nodes
    for t in T
}

PR = {
    (i, t):  renewable_p[i,t] if i in renewable_buses else 0

    for i in G_elec.nodes
    for t in T
}

QR = {
    (i, t):  renewable_q[i,t] if i in renewable_buses else 0

    for i in G_elec.nodes
    for t in T
}

PP = {
    (i, t): model.addVar(name='PP({})@{}'.format(i, t),
                         lb=PP_lims_lo[i],
                         ub=PP_lims_hi[i]) if i in water_pump_buses else 0

    for i in G_elec.nodes
    for t in T
}

QP = {
    (i, t): model.addVar(name='QP({})@{}'.format(i, t),
                         lb=QP_lims_lo[i],
                         ub=QP_lims_hi[i]) if i in water_pump_buses else 0

    for i in G_elec.nodes
    for t in T
}


PES = {
    (i, t): model.addVar(name='PES({})@{}'.format(i, t),
                         lb=-inf,
                         ub=inf) if i in battery_buses else 0

    for i in G_elec.nodes
    for t in T
}

QES = {
    (i, t): model.addVar(name='QES({})@{}'.format(i, t),
                         lb=-inf,
                         ub=inf) if i in battery_buses else 0

    for i in G_elec.nodes
    for t in T
}


PT = {
    (i, t): model.addVar(name='PT({})@{}'.format(i, t),
                         lb=PT_lims_lo[i],
                         ub=PT_lims_hi[i]) if i in power_to_gas_buses else 0

    for i in G_elec.nodes
    for t in T
}

QT = {
    (i, t): model.addVar(name='QT({})@{}'.format(i, t),
                         lb=QT_lims_lo[i],
                         ub=QT_lims_hi[i]) if i in power_to_gas_buses else 0

    for i in G_elec.nodes
    for t in T
}


#----------------------------------------------------------------------
# For all electrical lines
#----------------------------------------------------------------------
P = {
    (i, j, t): model.addVar(name='P({}->{})@{}'.format(i, j, t),
                            lb=-inf,
                            ub=inf)

    for (i, j) in G_elec.edges
    for t in T
}

Q = {
    (i, j, t): model.addVar(name='Q({}->{})@{}'.format(i, j, t),
                            lb=-inf,
                            ub=inf)

    for (i, j) in G_elec.edges
    for t in T
}

l = {
    (i, j, t): model.addVar(name='l({}->{})@{}'.format(i, j, t),
                            lb=0,
                            ub=l_lims[i,j])

    for (i, j) in G_elec.edges
    for t in T
}


#----------------------------------------------------------------------
# For all battery buses
#----------------------------------------------------------------------
LES = {
    (i, t): model.addVar(name='LES({})@{}'.format(i, t),
                         lb=0,
                         ub=inf)

    for i in battery_buses
    for t in T
}

EES = {
    (i, t): (battery_initial_soc[i] if t == t0 else
             model.addVar(name='EES({})@{}'.format(i,t),
                          lb=EES_lims_lo[i],
                          ub=EES_lims_hi[i]))
    for i in battery_buses
    for t in T_ext
}


#----------------------------------------------------------------------
# Electrical Constraints
#----------------------------------------------------------------------
model.addConstrs((
    sum(P[i,j,t]                     for j in G_elec.children_of(i)) -
    sum(P[k,i,t] - r[k,i] * l[k,i,t] for k in G_elec.parents_of(i))

    ==

    PG   [i,t] +
    PR   [i,t] +
    PES  [i,t] -
    PT   [i,t] -
    PL   [i,t] -
    PP   [i,t]

    for i in G_elec.nodes
    for t in T
), name='1')

model.addConstrs((
    sum(Q[i,j,t]                     for j in G_elec.children_of(i)) -
    sum(Q[k,i,t] - x[k,i] * l[k,i,t] for k in G_elec.parents_of(i))

    ==

    QG   [i,t] +
    QR   [i,t] +
    QES  [i,t] -
    QT   [i,t] -
    QL   [i,t] -
    QP   [i,t]

    for i in G_elec.nodes
    for t in T
), name='2')

model.addConstrs((
    v[i,t] - v[j,t]

    ==

    2 * r[i,j] * P[i,j,t] +
    2 * x[i,j] * Q[i,j,t] -
    z[i,j]**2 * l[i,j,t]

    for i in G_elec.nodes
    for j in G_elec.children_of(i)
    for t in T
), name='3')

model.addConstrs((
    P[i,j,t]**2 + Q[i,j,t]**2

    <=

    v[i,t] * l[i,j,t]

    for i in G_elec.nodes
    for j in G_elec.children_of(i)
    for t in T
), name='4')

model.addConstrs((
    s_lims[i,j]**2 * v[i,t] + sq_v_lims_lo[i] * sq_v_lims_hi[i] * l[i,j,t]

    <=

    s_lims[i,j]**2 * (sq_v_lims_lo[i] + sq_v_lims_hi[i])

    for i in G_elec.nodes
    for j in G_elec.children_of(i)
    for t in T
), name='5')

model.addConstrs((
    P[i,j,t]**2 + Q[i,j,t]**2

    <=

    s_lims[i,j]**2

    for i, j in G_elec.edges
    for t in T
), name='6')

model.addConstrs((
    (rbatt[i] + rcvt[i]) * PES[i,t]**2 + rcvt[i] * QES[i,t]**2

    <=

    LES[i,t] * v[i,t]

    for i in battery_buses
    for t in T
), name='7')

model.addConstrs((
    rbatt[i] * QES[i,t]**2 + sq_v_lims_lo[i] * LES[i,t]

    <=

    SES_lims[i]**2 * (rbatt[i] + rcvt[i])

    for i in battery_buses
    for t in T
), name='8')

model.addConstrs((
    SES_lims[i]**2 * v[i,t] + sq_v_lims_lo[i] * sq_v_lims_hi[i] * LES[i,t]

    <=

    SES_lims[i]**2 * (sq_v_lims_lo[i] + sq_v_lims_hi[i])

    for i in battery_buses
    for t in T
), name='9')

model.addConstrs((
    PES[i,t]**2 + QES[i,t]**2

    <=

    SES_lims[i]**2

    for i in battery_buses
    for t in T
), name='10')

model.addConstrs((
    EES[i,t] == EES[i,T_ext[d-1]] - PES[i,t] - LES[i,t]
    for i in battery_buses
    for d, t in enumerate(T_ext) if d != 0
), name='11')





#----------------------------------------------------------------------
# For all gas nodes
#----------------------------------------------------------------------
Pi = {
    (m, t): model.addVar(name='Pi({})@{}'.format(m, t),
                         lb=Pi_lims_lo[m],
                         ub=Pi_lims_hi[m])

    for m in G_gas.nodes
    for t in T
}

GLS = {
    (m, t): model.addVar(name='GLS({})@{}'.format(m, t),
                         lb=GLS_lims_lo[m],
                         ub=GLS_lims_hi[m]) if m in gas_supply_nodes else 0

    for m in G_gas.nodes
    for t in T
}


GT = {
    (m, t): model.addVar(name='GT({})@{}'.format(m, t),
                         lb=GT_lims_lo[m],
                         ub=GT_lims_hi[m]) if m in power_to_gas_nodes else 0

    for m in G_gas.nodes
    for t in T
}

GLch = {
    (m, t): model.addVar(name='GLch({})@{}'.format(m, t),
                         lb=0,
                         ub=GLch_lims[m]) if m in gas_storage_nodes else 0

    for m in G_gas.nodes
    for t in T
}

GLdis = {
    (m, t):  model.addVar(name='GLdis({})@{}'.format(m, t),
                          lb=0,
                          ub=GLdis_lims[m]) if m in gas_storage_nodes else 0

    for m in G_gas.nodes
    for t in T
}

GLG = {
    (m, t): model.addVar(name='GLG({})@{}'.format(m, t),
                         lb=GLG_lims_lo[m],
                         ub=GLG_lims_hi[m]) if m in gas_generator_nodes else 0

    for m in G_gas.nodes
    for t in T
}

tau = {
    (m, t): model.addVar(name='tau({})@{}'.format(m, t),
                         lb=0,
                         ub=inf) if m in compressor_line_source_nodes else 0

    for m in G_gas.nodes
    for t in T
}


#----------------------------------------------------------------------
# For all gas pipelines
#----------------------------------------------------------------------
GL = {
    (s, r, t): model.addVar(name='GL({}->{})@{}'.format(s, r, t),
                            lb=GL_lims_lo[s, r],
                            ub=GL_lims_hi[s, r])

    for (s, r) in G_gas.edges
    for t in T
}


#----------------------------------------------------------------------
# For all gas storage nodes
#----------------------------------------------------------------------
SOC = {
    (m, t): (gas_storage_initial_soc[m] if t == t0 else
             model.addVar(name='SOC({})@{}'.format(m, t),
                          lb=SOC_lims_lo[m],
                          ub=SOC_lims_hi[m]))

    for m in gas_storage_nodes
    for t in T_ext
}


#----------------------------------------------------------------------
# Gas constraints
#----------------------------------------------------------------------
model.addConstrs((
    GLS[m,t]                                     +
    GT[m,t]                                      +
    sum(GL[s,m,t] for s in G_gas.parents_of(m))  -
    sum(GL[m,r,t] for r in G_gas.children_of(m)) +
    GLdis[m,t]                                   -
    GLch[m,t]

    ==

    tau[m,t]  +
    Dgas[m,t] +
    GLG[m,t]

    for m in G_gas.nodes
    for t in T
), name='12')

model.addConstrs((
    GL[s,r,t] == Phi[s,r](Pi[s,t], Pi[r,t])

    for (s, r) in G_gas.edges if (s, r) not in compressor_lines
    for t in T
), name='13')

model.addConstrs((
    Pi[s,t] <= Pi[r,t]

    for (s, r) in compressor_lines
    for t in T
), name='14')

sigma1=1.17E-04
sigma2=2.24E-05
sigma3=-2.24E-05
sigma4=0.007053
model.addConstrs((
    tau[s,t]

    ==

    sigma1 * GL[s,r,t] + sigma2 * Pi[r,t] + sigma3 * Pi[s,t] + sigma4

    for (s, r) in compressor_lines
    for t in T
), name='15')

model.addConstrs((
    SOC[m,t] == SOC[m,T_ext[d-1]] + eta_G * GLch[m,t] - 1/eta_G * GLdis[m,t]

    for m in gas_storage_nodes
    for d, t in enumerate(T_ext) if d != 0
), name='16')


#----------------------------------------------------------------------
# For all water nodes
#----------------------------------------------------------------------
y = {

    (k, t): model.addVar(name='y({})@{}'.format(k, t),
                         lb=y_lims_lo[k],
                         ub=y_lims_hi[k])

    for k in G_water.nodes
    for t in T
}

fG = {
    (k, t): model.addVar(name='fG({})@{}'.format(k, t),
                         lb=fG_lims_lo[k],
                         ub=fG_lims_hi[k]) if k in water_supply_nodes else 0

    for k in G_water.nodes
    for t in T
}

fT = {
    (k, t): model.addVar(name='fT({})@{}'.format(k, t),
                         lb=fT_lims_lo[k],
                         ub=fT_lims_hi[k]) if k in water_storage_nodes else 0

    for k in G_water.nodes
    for t in T
}


#----------------------------------------------------------------------
# For all water pipelines
#----------------------------------------------------------------------
f = {
    (k, n, t): model.addVar(name='f({}->{})@{}'.format(k, n, t),
                            lb=f_lims_lo[k,n],
                            ub=f_lims_hi[k,n])

    for (k, n) in G_water.edges
    for t in T
}

#----------------------------------------------------------------------
# For all pump-enabled pipelines
#----------------------------------------------------------------------
alpha = {
    (k, n, t): model.addVar(name='alpha({}->{})@{}'.format(k, n, t),
                            vtype=gurobi.GRB.BINARY)

    for (k, n) in water_pump_lines
    for t in T
}

yG = {
    (k, n, t): model.addVar(name='yG({}->{})@{}'.format(k, n, t),
                            lb=-inf,
                            ub=inf)

    for (k, n) in water_pump_lines
    for t in T
}

#----------------------------------------------------------------------
# For all water storage nodes
#----------------------------------------------------------------------
SW = {
    (k, t): (water_storage_initial_soc[k] if t == t0 else
             model.addVar(name='SW({})@{}'.format(k, t),
                          lb=SW_lims_lo[k],
                          ub=SW_lims_hi[k]))

    for k in water_storage_nodes
    for t in T_ext
}


#----------------------------------------------------------------------
# Water constraints
#----------------------------------------------------------------------
model.addConstrs((
    sum(f[s,k,t] for s in G_water.parents_of(k)) +
    fG[k,t]

    ==

    sum(f[k,r,t] for r in G_water.children_of(k)) +
    fT[k,t]                                       +
    dW[k,t]


    for k in G_water.nodes
    for t in T
), name='17')

model.addConstrs((
    y[k,t] - y[n,t] +
    h[k]   - h[n]

    <=

    (2* 2**0.5 - 2) * RP[k,n] * f_lims_hi[k,n] * f[k,n,t] +
    (3 - 2* 2**0.5) * RP[k,n] * f_lims_hi[k,n]

    for (k, n) in G_water.edges if (k, n) not in water_pump_lines
    for t in T
), name='18')

model.addConstrs((
    y[k,t] - y[n,t] +
    h[k]   - h[n]

    >=

    (2* 2**0.5 - 2) * RP[k,n] * f_lims_lo[k,n] * f[k,n,t] +
    (3 - 2* 2**0.5) * RP[k,n] * f_lims_lo[k,n]

    for (k, n) in G_water.edges if (k, n) not in water_pump_lines
    for t in T
), name='19')

model.addConstrs((
    y[k,t] - y[n,t] +
    h[k]   - h[n]

    >=

    2* RP[k,n] * f_lims_hi[k,n] * f[k,n,t] -
    RP[k,n] * f_lims_hi[k,n]**2

    for (k, n) in G_water.edges if (k, n) not in water_pump_lines
    for t in T
), name='20')

model.addConstrs((
    y[k,t] - y[n,t] +
    h[k]   - h[n]

    >=

    2* RP[k,n] * f_lims_lo[k,n] * f[k,n,t] -
    RP[k,n] * f_lims_lo[k,n]**2

    for (k, n) in G_water.edges if (k, n) not in water_pump_lines
    for t in T
), name='21')

M1 = 1e12
model.addConstrs((
    f[k,n,t]

    <=

    alpha[k,n,t] * M1

    for (k, n) in water_pump_lines
    for t in T
), name='22')

model.addConstrs((
    yG[k,n,t]

    ==

    Phi_W[k,n](f[k,n,t])

    for (k, n) in water_pump_lines
    for t in T
), name='23')


M2 = 1e12
AW = {
    (k, n, t): (
        y[k,t] - y[n,t] + h[k] - h[n] + yG[k,n,t] + M2 * (1 - alpha[k,n,t])
    )

    for (k, n) in water_pump_lines
    for t in T
}

BW = {
    (k, n, t): (
        y[k,t] - y[n,t] + h[k] - h[n] + yG[k,n,t] + M2 * (alpha[k,n,t] - 1)
    )

    for (k, n) in water_pump_lines
    for t in T
}

model.addConstrs((
    RP[k,n] * f[k,n,t]**2 - AW[k,n,t] <= 0

    for (k, n) in water_pump_lines
    for t in T
), name='24')

model.addConstrs((
    BW[k,n,t] - RP[k,n] * f_lims_hi[k,n] * f[k,n,t] <= 0

    for (k, n) in water_pump_lines
    for t in T
), name='25')


model.addConstrs((
    SW[k, t] == SW[k, T_ext[d-1]] + fT[k,t]

    for k in water_storage_nodes
    for d, t in enumerate(T_ext) if d != 0
), name='26')


#----------------------------------------------------------------------
# Coupling constraints
#----------------------------------------------------------------------
model.addConstrs((
    PG[i,t]

    ==

    eta_G2P * GLG[m,t] * HHVSNG

    for i, m in gas_generator_mappings.items()
    for t in T
), name='27')

model.addConstrs((
    GT[m,t]

    ==

    eta_P2G * PT[i,t] / HHVSNG

    for i, m in power_to_gas_mappings.items()
    for t in T
), name='28')

model.addConstrs((
    eta_W[i] * PP[i,t]

    >=

    Phi_W[k,n](f[k,n,t]) * f[k,n,t]

    for i, (k, n) in water_pump_mappings.items()
    for t in T
), name='29')

model.addConstrs((
    eta_W[i] * PP[i,t]

    <=

    Phi_W[k,n](f_lims_hi[k,n]) * f[k,n,t]

    for i, (k, n) in water_pump_mappings.items()
    for t in T
), name='30')

#----------------------------------------------------------------------
# Objective
#----------------------------------------------------------------------
model.setObjective(sum(
    sum(Ce[i](PG[i,t],t)  for i in generator_buses) +
    sum(Cg[m](GLS[m,t],t) for m in gas_supply_nodes)

    for t in T
), gurobi.GRB.MINIMIZE)


model.optimize()
model.display()


print('{}\n# {}\n{}'.format('#'*70, 'Results', '#'*70))
print('objective: {}'.format(model.getObjective().getValue()))

for v in model.getVars():
    print('{:<60}= {}'.format(v.VarName, v.X))
