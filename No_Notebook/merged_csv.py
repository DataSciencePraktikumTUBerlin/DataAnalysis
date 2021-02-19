# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:33:11 2021

@author: Roberto (from Stefan)
"""

import os
import numpy as np
import pandas as pd

folder = './csv'
files = os.listdir(folder)

df = pd.DataFrame()

#df_dict={}

for file in files:
    file = f'{folder}/{file}'
    
    if df.size == 0:
        df = pd.read_csv(file, index_col=0)
        print(file)

        continue
        
    df2 = pd.read_csv(file, index_col=0)
#    df_dict[file]=df2
    df = df.merge(df2, on=['Country', 'Years'], how='left')

#df = df.replace('..', np.nan).fillna(method='ffill')

# check if cumilated data
for c in df.columns:
#    if c in ['Country', 'Year']:
#        continue
        
    print(c)#df[c].is_monotonic)#_increasing)
    
#df.to_csv('./energy.csv')