#!/usr/bin/env Python3
FEET_PER_MILE = 5280
FEET_PER_METER = 3.28084
PSI_PER_BAR = 14.5038

def feet_to_miles(feet):
    miles = feet / FEET_PER_MILE
    return miles

def cubic_meters_to_cubic_feet(cubic_meters):
    CUBIC_FEET_PER_CUBIC_METER = FEET_PER_METER**3
    cubic_feet = cubic_meters * CUBIC_FEET_PER_CUBIC_METER
    return cubic_feet

# from Thousand Cubic Meters Per Hour (MCM/h)
# to   Thousand Cubic Feet Per Hour (MCF/h)
mcmph_to_mcfph = cubic_meters_to_cubic_feet

def bar_to_psi(bar):
    psi = bar * PSI_PER_BAR
    return psi
