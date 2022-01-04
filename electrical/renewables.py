#!/usr/bin/env python3

renewable_buses = {
    '633',
    '680',
}


p_renewables = {
    # (bus, time): watts
    ('633', '2022-01-01T00:00:00Z'): 100E3,
    ('633', '2022-01-01T00:01:00Z'): 110E3,

    ('680', '2022-01-01T00:00:00Z'): 200E3,
    ('680', '2022-01-01T00:01:00Z'): 220E3,
}


q_renewables = {
    # (bus, time): vars
    ('633', '2022-01-01T00:00:00Z'): 100E3,
    ('633', '2022-01-01T00:01:00Z'): 110E3,

    ('680', '2022-01-01T00:00:00Z'): 200E3,
    ('680', '2022-01-01T00:01:00Z'): 220E3,
}
