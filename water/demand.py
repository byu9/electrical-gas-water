#!/usr/bin/env python3
from misc.unit_conversions import gpm_to_gph

demand = {
    # (node, time): demand_gph
    ('1', '2022-01-01T00:00:00Z'): gpm_to_gph(0),
    ('2', '2022-01-01T00:00:00Z'): gpm_to_gph(0),
    ('3', '2022-01-01T00:00:00Z'): gpm_to_gph(150),
    ('4', '2022-01-01T00:00:00Z'): gpm_to_gph(150),
    ('5', '2022-01-01T00:00:00Z'): gpm_to_gph(200),
    ('6', '2022-01-01T00:00:00Z'): gpm_to_gph(150),
    ('7', '2022-01-01T00:00:00Z'): gpm_to_gph(0),
    ('8', '2022-01-01T00:00:00Z'): gpm_to_gph(0),

    ('1', '2022-01-01T00:01:00Z'): gpm_to_gph(0),
    ('2', '2022-01-01T00:01:00Z'): gpm_to_gph(0),
    ('3', '2022-01-01T00:01:00Z'): gpm_to_gph(150),
    ('4', '2022-01-01T00:01:00Z'): gpm_to_gph(150),
    ('5', '2022-01-01T00:01:00Z'): gpm_to_gph(200),
    ('6', '2022-01-01T00:01:00Z'): gpm_to_gph(150),
    ('7', '2022-01-01T00:01:00Z'): gpm_to_gph(0),
    ('8', '2022-01-01T00:01:00Z'): gpm_to_gph(0),
}
