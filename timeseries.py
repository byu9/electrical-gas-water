#!/usr/bin/env python3

#----------------------------------------------------------------------
# Specify scheduling horizon in the following format
# [t1, t2, ...]
#
# Make sure the time points are unique and hashable, and that the list
# is incremental.
#
# Discussion with Xiaochu about unit of measure:
#       Period in the scheduling horizon must be 1 hour.
#----------------------------------------------------------------------
scheduling_horizon = [
    '2022-01-01T00:00:00Z',
    '2022-01-01T00:01:00Z',
]
