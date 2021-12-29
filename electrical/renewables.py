#!/usr/bin/env python3

renewable_buses = {
    '645',
    '680',
}


p_renewables = {
    #----------------------------------------------------------------------
    # Specify renewables in the following format
    # (bus, time): watts
    #
    # Unspecified buses do not have renewables. Make sure to specify all the
    # time points in the scheduling horizon.
    #----------------------------------------------------------------------
    ('645', '2022-01-01T00:00:00Z'): 11.45E3,
    ('645', '2022-01-01T00:01:00Z'): 11.44E3,

    ('680', '2022-01-01T00:00:00Z'): 12.36E3,
    ('680', '2022-01-01T00:01:00Z'): 12.37E3,
}


q_renewables = {
    #----------------------------------------------------------------------
    # Specify renewables in the following format
    # (bus, time): vars
    #
    # Unspecified buses do not have renewables. Make sure to specify all the
    # time points in the scheduling horizon.
    #----------------------------------------------------------------------
    ('645', '2022-01-01T00:00:00Z'): 1.34E3,
    ('645', '2022-01-01T00:01:00Z'): 1.35E3,

    ('680', '2022-01-01T00:00:00Z'): 2.92E3,
    ('680', '2022-01-01T00:01:00Z'): 2.91E3,
}
