# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:17:44 2021

MERGING PREPROCESSED CSVS

@author: Roberto
"""
import pandas as pd
import numpy as np

e = pd.read_csv('energy_DF.csv', index_col=0)
f = pd.read_csv('finance_DF.csv', index_col=0)

#e = e.groupby('Year').sum()
#f = f.groupby('Year').sum()

years = np.arange(2004, 2016)

e = e[e.Year.isin(years)]
f = f[f.Year.isin(years)]

df = e.merge(f, on=['Year', 'Country'], how = 'inner')
    
df.to_csv('./Big_DF.csv')