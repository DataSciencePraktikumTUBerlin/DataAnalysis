# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:35:00 2021

from Stefan's Notebook

@author: Roberto
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')
"""
TO NOTICE:
    sns.set_theme(style='darkgrid')
    https://github.com/mwaskom/seaborn/issues/2301
"""

e = pd.read_csv('energy_DF.csv', index_col=0)
f = pd.read_csv('finance_DF.csv', index_col=0)

e = e.groupby('Year').sum()
f = f.groupby('Year').sum()

#selectpairs if necessary
sel_e = ['Energy intensity-primary energy',
       'Renewable share electricity output',
       'Renewables-Consumption Prim Energy']
sel_f = ['Corporate R&D',
       'Asset Finance minus Re-invested equity',
       'Number of policies']

years = np.arange(2004, 2016)

e = e[sel_e].loc[years]
f = f[sel_f].loc[years]

plt.figure(figsize=(12, 12))

corr = pd.concat([e, f], axis=1, keys=['e', 'f']).corr().loc['f', 'e']
# mask = np.triu(np.ones_like(corr, dtype=bool))

h = sns.heatmap(corr, vmin=-1, vmax=1, annot=True, cmap='BrBG', annot_kws={"size":30})
h.set_xticklabels(h.get_xticklabels(), rotation=15, ha='right', fontsize=14)
h.set_yticklabels(h.get_yticklabels(), rotation=70, ha='right', fontsize=14)

# Save the figure
plt.savefig("resume_correlogram.jpg")#"resume_correlogram.jpg")

c_corr_list = list()#c_c for c_c in corr.iteritems()]

for ccf_e, ccf_f in corr.iteritems():
    for ccf, cval in ccf_f.iteritems():
        label = f"Pair:{ccf_e}-{ccf}"
        element = [tuple((label, cval))]
        c_corr_list = c_corr_list + element
        
c_corr_list90 = [(c_corr[0],round(c_corr[1],3)) for c_corr  in c_corr_list if abs(c_corr[1])>0.92]

c_corr_list96 = [(c_corr[0],round(c_corr[1],3)) for c_corr  in c_corr_list if abs(c_corr[1])>0.96]    

c_corr_list98 = [(c_corr[0],round(c_corr[1],3)) for c_corr  in c_corr_list if abs(c_corr[1])>0.98]

# Print top correlations

MyFile=open('Top_correlations.txt','w')

MyFile.write('Coef>0.9 = ')
MyFile.write(str(len(c_corr_list90)))
MyFile.write('\n')
for element in c_corr_list90:
     MyFile.write(str(element))
     MyFile.write('\n')
     
MyFile.write('\n')
MyFile.write('Coef>0.96 = ')
MyFile.write(str(len(c_corr_list96)))
MyFile.write('\n')
for element in c_corr_list96:
     MyFile.write(str(element))
     MyFile.write('\n')
     
MyFile.write('\n')
MyFile.write('Coef>0.98 = ')
MyFile.write(str(len(c_corr_list98)))
MyFile.write('\n')
for element in c_corr_list98:
     MyFile.write(str(element))
     MyFile.write('\n')
     
MyFile.close()