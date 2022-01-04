#!/usr/bin/env python3

def feet_to_miles(feet):
    FEET_PER_MILE = 5280
    miles = feet / FEET_PER_MILE
    return miles


lines = {
    # (from_bus, to_bus): (line_type, miles)
    ('632', '645'): ('603', feet_to_miles(500)),
    ('632', '633'): ('602', feet_to_miles(500)),
    # transformer impedance to be stored as per-mile for convenience
    ('633', '634'): ('XFM-1', 1),
    ('645', '646'): ('603', feet_to_miles(300)),
    ('650', '632'): ('601', feet_to_miles(2000)),
    ('684', '652'): ('607', feet_to_miles(800)),
    ('632', '671'): ('601', feet_to_miles(2000)),
    ('671', '684'): ('604', feet_to_miles(300)),
    ('671', '680'): ('601', feet_to_miles(1000)),
    # switch impedance to be stored as per-mile for convenience
    ('671', '692'): ('Switch', 1),
    ('684', '611'): ('605', feet_to_miles(300)),
    ('692', '675'): ('606', feet_to_miles(500)),
    # substation impedance to be stored as per-mile for convenience
    ('Grid', '650'): ('Substation', 1),
}



def per_unit_to_ohms(pu, volt_amp, volt):
    ohms_base = volt**2 / volt_amp
    ohms = pu * ohms_base
    return ohms

# Per Xiaochu, assume single phase using phase C data
z_per_mile_by_type = {
    # line_type: ohms_per_mile
    '601': 0.3414 + 1.0348j,
    '602': 0.7436 + 1.2112j,
    '603': 1.3238 + 1.3569j,
    '604': 1.3294 + 1.3471j,
    '605': 1.3292 + 1.3475j,
    '606': 0.7982 + 0.4463j,
    # does not have C phase. A used instead.
    '607': 1.3425 + 0.5124j,

    # stored as per-mile for convenience
    # ohms at 4.16kV side
    # Per Junkai, normalizing to the primary side to avoid per-unit
    'XFM-1': per_unit_to_ohms(pu=(1.1+2j)/100,
                              volt_amp=500E3, volt=4.16E3),

    # stored as per-mile for convenience
    # Per Xiaochu, the switch is always closed
    'Switch': 0,

    # stored as per-mile for convenience
    # ohms at 4.16kV side
    'Substation': per_unit_to_ohms(pu=(1+8j)/100,
                                   volt_amp=5E6, volt=4.16E3),
}

# Per Xiaochu, assume single phase using phase C data
b_per_mile_by_type= {
    # line_type: pi_model_siemens_per_mile
    '601': 5.6386E-3,
    '602': 5.4246E-3,
    '603': 4.6658E-3,
    '604': 4.7097E-3,
    '605': 4.5193E-3,
    '606': 96.8897E-3,
    # does not have C phase. A used instead.
    '607': 88.9912E-3,
    'XFM-1': 0,
    'Switch': 0,
    'Substation': 0,
}




i_lim_by_type = {
    # line_type: amps

    # Per Junkai, using 10kA as placeholder
    '601': 10E3,
    '602': 10E3,
    '603': 10E3,
    '604': 10E3,
    '605': 10E3,
    '606': 10E3,
    '607': 10E3,
    'XFM-1': 10E3,
    'Switch': 10E3,
    'Substation': 10E3,
}


s_lim_by_type = {
    # line_type: volt_amps
    # Per Junkai, using 10MVA as placeholder
    '601': 10E6,
    '602': 10E6,
    '603': 10E6,
    '604': 10E6,
    '605': 10E6,
    '606': 10E6,
    '607': 10E6,
    'XFM-1': 10E6,
    'Switch': 10E6,
    'Substation': 10E6,
}



#----------------------------------------------------------------------
# Applies line type mapping
#----------------------------------------------------------------------
line_z = {
    line: z_per_mile_by_type[line_type] * miles
    for line, (line_type, miles) in lines.items()
}

line_r = {line: z.real for line, z in line_z.items()}
line_x = {line: z.imag for line, z in line_z.items()}

line_i_lims = {
    line: i_lim_by_type[line_type]
    for line, (line_type, _) in lines.items()
}

line_s_lims = {
    line: s_lim_by_type[line_type]
    for line, (line_type, _) in lines.items()
}
