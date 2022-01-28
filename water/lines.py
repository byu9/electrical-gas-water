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
    ('2', '3'): (300, 20, 100),
    ('3', '7'): (500, 20, 100),
    ('3', '4'): (500, 20, 100),
    ('4', '6'): (500, 20, 100),
    ('6', '7'): (500, 20, 100),
    ('4', '5'): (500, 20, 100),
    ('5', '6'): (700, 20, 100),
    ('7', '8'): (700, 20, 100),

    # pump-enabled pipelines
    ('1', '2'): (500, 20, 100),
}


# pressure-flow relationship for constant-speed pumps
def constant_speed_pump_pres(flow_gph, a1, a0):
    pres_ftw = a1 * flow_gph + a0
    return pres_ftw



pump_induced_pres_funcs = {
    # (pipe_s, pipe_r): callable(flow_gph) -> pres_ftw
    ('1', '2'): lambda flow: constant_speed_pump_pres(flow,
                                                      a1=-0, a0=230),
}



def calc_pres_loss_coeff(len_ft, diameter_inches):
    GRAVITATIONAL_ACCELERATION = 32.2
    CONCRETE_PIPE_ENTRANCE_HEADLOSS_COEFFICIENT = 0.2

    SECONDS_PER_HOUR = 3600
    INCHES_PER_FOOT = 12
    CUBIC_INCHES_PER_GALLON = 231

    radius_inches = diameter_inches / 2
    cross_section_squared_inches = radius_inches**2 * pi

    FOOT_PER_SECOND_VELOCITY_PER_GPH = (
        # 1 GPH *
        CUBIC_INCHES_PER_GALLON / cross_section_squared_inches /
        INCHES_PER_FOOT / SECONDS_PER_HOUR
    )

    g = GRAVITATIONAL_ACCELERATION
    Ke = CONCRETE_PIPE_ENTRANCE_HEADLOSS_COEFFICIENT

    pres_loss_coeff = Ke / (2*g) * FOOT_PER_SECOND_VELOCITY_PER_GPH**2

    return pres_loss_coeff


pres_loss_coeffs = {
    pipe: calc_pres_loss_coeff(L, D)

    for pipe, (L, D, _) in pipe_params.items()
}
