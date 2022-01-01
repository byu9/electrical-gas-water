#!/usr/bin/env python3

from pandas import read_csv

df_load_kw = read_csv('electrical/tables/load_kw.csv',
                      parse_dates=[0]).set_index('t')

df_load_kvar = read_csv('electrical/tables/load_kvar.csv',
                        parse_dates=[0]).set_index('t')

df_load_watts = df_load_kw * 1E3
df_load_vars = df_load_kvar * 1E3

p_loads = df_load_watts.transpose().stack()
q_loads = df_load_vars.transpose().stack()
