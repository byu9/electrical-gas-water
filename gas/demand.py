#!/usr/bin/env python3

gas_demands = {
    # (node, time): mcf_per_hour
    ('entry01' , '2022-01-01T00:00:00Z'): 10,
    ('entry02' , '2022-01-01T00:00:00Z'): 20,
    ('entry03' , '2022-01-01T00:00:00Z'): 30,
    ('exit01'  , '2022-01-01T00:00:00Z'): 15,
    ('exit02'  , '2022-01-01T00:00:00Z'): 25,
    ('exit03'  , '2022-01-01T00:00:00Z'): 35,
    ('N01'     , '2022-01-01T00:00:00Z'): 16,
    ('N02'     , '2022-01-01T00:00:00Z'): 26,
    ('N03'     , '2022-01-01T00:00:00Z'): 36,
    ('N04'     , '2022-01-01T00:00:00Z'): 46,
    ('N05'     , '2022-01-01T00:00:00Z'): 56,

    ('entry01' , '2022-01-01T00:01:00Z'): 10,
    ('entry02' , '2022-01-01T00:01:00Z'): 20,
    ('entry03' , '2022-01-01T00:01:00Z'): 30,
    ('exit01'  , '2022-01-01T00:01:00Z'): 15,
    ('exit02'  , '2022-01-01T00:01:00Z'): 25,
    ('exit03'  , '2022-01-01T00:01:00Z'): 35,
    ('N01'     , '2022-01-01T00:01:00Z'): 16,
    ('N02'     , '2022-01-01T00:01:00Z'): 26,
    ('N03'     , '2022-01-01T00:01:00Z'): 36,
    ('N04'     , '2022-01-01T00:01:00Z'): 46,
    ('N05'     , '2022-01-01T00:01:00Z'): 56,
}
