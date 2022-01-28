#!/usr/bin/env python3
from misc.unit_conversions import (
    psi_per_gpm2_to_ftw_per_gph2,
    gpm_to_gph,
)

from math import pi



flow_lims = {
    # (s, r): (gal_per_h_lo, gal_per_h_hi)

    ('2', '3'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('3', '7'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('3', '4'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('4', '6'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('6', '7'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('4', '5'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('5', '6'): (gpm_to_gph(-6000), gpm_to_gph(6000)),
    ('7', '8'): (gpm_to_gph(-6000), gpm_to_gph(6000)),

    # pump-enabled pipelines
    ('1', '2'): (gpm_to_gph(0),    gpm_to_gph(6000)),
}

flow_lims_lo = dict()
flow_lims_hi = dict()
for node, (lo, hi) in flow_lims.items():
    flow_lims_lo[node] = lo
    flow_lims_hi[node] = hi


water_pump_lines = {
    # (s, r),
    ('1', '2'),
}

pipe_params = {
    # (pipe_s, pipe_r): (length_ft, diameter_inches, roughness_c_factor)
    ('2', '3'): (3000, 14, 100),
    ('3', '7'): (5000, 12, 100),
    ('3', '4'): (5000, 8,  100),
    ('4', '6'): (5000, 8,  100),
    ('6', '7'): (5000, 8,  100),
    ('4', '5'): (5000, 6,  100),
    ('5', '6'): (7000, 6,  100),
    ('7', '8'): (7000, 10, 100),

    # pump-enabled pipelines
    ('1', '2'): (5000, 6,  100),
}


# pressure-flow relationship for constant-speed pumps
def constant_speed_pump_pres(flow_gph, a1, a0):
    pres_ftw = a1 * flow_gph + a0
    return pres_ftw



pump_induced_pres_funcs = {
    # (pipe_s, pipe_r): callable(flow_gph) -> pres_ftw
    ('1', '2'): lambda flow: constant_speed_pump_pres(flow,
                                                      a1=-1.5, a0=300),
}



def calc_pres_loss_coeff(len_ft, diameter_inches):
    # in ft/s^2
    GRAVITATIONAL_ACCELERATION = 32.2

    g = GRAVITATIONAL_ACCELERATION
    L = len_ft
    D = diameter_inches

    # based on PSI/GPM^2
    pres_loss_coeff = 8 * 890.9 * L / (pi**2 * g * D * 1E4)

    # to feet-water-column-per-(gallons_per_hour)^2
    pres_loss_coeff = psi_per_gpm2_to_ftw_per_gph2(pres_loss_coeff)

    return pres_loss_coeff


pres_loss_coeffs = {
    pipe: calc_pres_loss_coeff(L, D)

    for pipe, (L, D, _) in pipe_params.items()
}
