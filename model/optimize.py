#!/usr/bin/env python3
import gurobipy as gurobi
from topology import (
    digraph as G,
    lines,
    Line,
    line_r as r,
    line_x as x,
)

# scheduling horizon
T = ['2022-01-01 00:00'] # placeholder



model = gurobi.Model()

#----------------------------------------------------------------------
# constants
#----------------------------------------------------------------------
PR = {
    # (bus, time): renewable generation
    (i, t): 1.11

    for i in G.nodes
    for t in T
}

QR = {
    # (bus, time): renewable generation
    (i, t): 2.22

    for i in G.nodes
    for t in T
}

PL = {
    # (bus, time): load
    (i, t): 3.33

    for i in G.nodes
    for t in T
}

QL = {
    # (bus, time): load
    (i, t): 4.44

    for i in G.nodes
    for t in T
}


#----------------------------------------------------------------------
# creates decision variables
#
# Stored as name value pairs to be easily indexed/referenced later.
#----------------------------------------------------------------------
P = {
    (l, t): model.addVar(name='P of {} at t={}'.format(repr(l), t))

    for l in lines
    for t in T
}

Q = {
    (l, t): model.addVar(name='Q of {} at t={}'.format(repr(l), t))

    for l in lines
    for t in T
}

l = {
    (l, t): model.addVar(name='I^2 of {} at t={}'.format(repr(l), t))

    for l in lines
    for t in T
}

PG = {
    (i, t): model.addVar(name='G2P P of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

QG = {
    (i, t): model.addVar(name='G2P Q of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

Pdis = {
    (i, t): model.addVar(name='Batt. dis. P of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

Qdis = {
    (i, t): model.addVar(name='Batt. dis. Q of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}


Pch = {
    (i, t): model.addVar(name='Batt. ch. P of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

Qch = {
    (i, t): model.addVar(name='Batt. ch. Q of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

PT = {
    (i, t): model.addVar(name='P2G P of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

QT = {
    (i, t): model.addVar(name='P2G Q of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

PP = {
    (i, t): model.addVar(name='Water P of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

QP = {
    (i, t): model.addVar(name='Water Q of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}

v = {
    (i, t): model.addVar(name='V^2 of {} at t={}'.format(i, t))

    for i in G.nodes
    for t in T
}


#----------------------------------------------------------------------
# Gas powered generator cost coefficients
#----------------------------------------------------------------------
Cp_coeffs = {
    # bus: (a, b, c)
    # omit buses without the generator
    i: (0.001, 0.01, 0.1)
    
    for i in G.nodes
}

def gas_gen_cost(PG, a, b, c):
    return a*PG**2 + b*PG + c

# dictionary of callables
Cp = {
    # bus: Cp(PG) Cost Cp of operating at PG
    i:
    (lambda PG: gas_gen_cost(PG, *Cp_coeffs[i])) if i in Cp_coeffs.keys() else
    # handles buses without the generator
    (lambda PG: 0)

    for i in G.nodes
}

#----------------------------------------------------------------------
# Creates objective
#----------------------------------------------------------------------
model.setObjective(sum(
    sum(Cp[i](PG[i, t]) for i in G.nodes)
    # TODO add gas system
    for t in T
))


#----------------------------------------------------------------------
# Creates constraints
#----------------------------------------------------------------------
# 1a
model.addConstrs(
    (sum(P[Line(i, j), t] for j in G.children_of(i)) -
     sum(P[Line(k, i), t] - r[Line(k, i)] * l[Line(k, i), t]
         for k in G.parents_of(i)))

    ==

    (PG[i, t] +PR[i, t] +Pdis[i, t] -PT[i, t] -PL[i, t] -PP[i, t] -Pch[i, t])

    for i in G.nodes
    for t in T
)

# 1b
model.addConstrs(
    (sum(Q[Line(i, j), t] for j in G.children_of(i)) -
     sum(Q[Line(k, i), t] - x[Line(k, i)] * l[Line(k, i), t]
         for k in G.parents_of(i)))

    ==

    (QG[i, t] +QR[i, t] +Qdis[i, t] -QT[i, t] -QL[i, t] -QP[i, t] -Qch[i, t])

    for i in G.nodes
    for t in T
)


# 1c
model.addConstrs(
    (v[i, t] -v[j, t])

    ==

    (2 * r[Line(i, j)] * P[Line(i, j), t] +
     2 * x[Line(i, j)] * Q[Line(i, j), t] -
     (r[Line(i, j)]**2 + x[Line(i, j)]**2) * l[Line(i, j), t])

    for i in G.nodes
    for j in G.children_of(i)
    for t in T
)

# 1e
model.addConstrs(
    (P[Line(i, j), t]**2 + Q[Line(i, j), t]**2)

    <=

    (v[i, t] * l[Line(i, j), t])

    for i in G.nodes
    for j in G.children_of(i)
    for t in T
)

# # 1f
# model.addConstrs(
    
#     for i in G.nodes
#     for j in children_of(i)
#     for t in T
# )

# # 1g
# model.addConstrs(
    
#     for l in lines,
#     for t in T
# )

# # 1h
# model.addConstrs(

#     for l in lines
#     for t in T
# )

# # 1i
# model.addConstrs(

#     for i in G.nodes
#     for t in T
# )

model.optimize()


for i in [P, Q, l, PG, QG, Pdis, Qdis, PT, QT, PP, QP, Pch, Qch]:
    print('\n'.join('{}: {}'.format(v.VarName, v.X) for k, v in i.items()))


