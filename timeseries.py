#!/usr/bin/env python3

#----------------------------------------------------------------------
# Specify scheduling horizon in the following format
# [t1, t2, ...]
#
# Make sure the time points are unique and hashable, and that the list
# is incremental. The scheduling horizon must not contain 'None' as an
# element because it is used to create the extended scheduling horizon
#
# Discussion with Xiaochu about unit of measure:
#       Period in the scheduling horizon must be 1 hour.
#----------------------------------------------------------------------
scheduling_horizon = [
    '2022-01-01T00:00:00Z',
    '2022-01-01T00:01:00Z',
]

# Prepends timepoint 'None'. This is useful for indexing the initial state (a
# constant) the same way as decision variables for the scheduling horizon.
extended_initial_timepoint = None
extended_scheduling_horizon = [extended_initial_timepoint] + scheduling_horizon
