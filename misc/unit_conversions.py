#!/usr/bin/env Python3
FEET_PER_MILE = 5280
FEET_PER_METER = 3.28084
PSI_PER_BAR = 14.5038
MINUTE_PER_HOUR = 60
FEET_WATER_COLUMN_PER_PSI = 2.31

def feet_to_miles(feet):
    miles = feet / FEET_PER_MILE
    return miles

def cubic_meters_to_cubic_feet(cubic_meters):
    CUBIC_FEET_PER_CUBIC_METER = FEET_PER_METER**3
    cubic_feet = cubic_meters * CUBIC_FEET_PER_CUBIC_METER
    return cubic_feet

def x_per_minute_to_x_per_hour(x_per_minute):
    x_per_hour = x_per_minute * MINUTE_PER_HOUR
    return x_per_hour

# from Thousand Cubic Meters Per Hour (MCM/h)
# to   Thousand Cubic Feet Per Hour (MCF/h)
mcmph_to_mcfph = cubic_meters_to_cubic_feet

def bar_to_psi(bar):
    psi = bar * PSI_PER_BAR
    return psi

# from Gallons Per Minute
# to   Gallons Per Hour
gpm_to_gph = x_per_minute_to_x_per_hour


# from PSI               Per (Gallon Per Minute)^2
# to   Feet water column Per (Gallon Per Hour)^2

def psi_per_gpm2_to_ftw_per_gph2(psi_per_gpm2):
    CONVERSION_COEFF = (FEET_WATER_COLUMN_PER_PSI /
                        MINUTE_PER_HOUR**2)

    ftw_per_gph2 = CONVERSION_COEFF * psi_per_gpm2
    return ftw_per_gph2
