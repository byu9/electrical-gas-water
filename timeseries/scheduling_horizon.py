#!/usr/bin/env python3

#----------------------------------------------------------------------
# Specify scheduling horizon in the following format
# [t1, t2, ...]
#
# Make sure the time points are unique and hashable, and that the list
# is incremental.
#----------------------------------------------------------------------
from pandas import read_csv

df_scheduling_horizon = read_csv('timeseries/tables/scheduling_horizon.csv',
                                 parse_dates=[0]).set_index('t')

scheduling_horizon = df_scheduling_horizon.index
