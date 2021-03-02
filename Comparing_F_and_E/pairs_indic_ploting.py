# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 22:15:59 2021

Generate scatter plot for the selected indicators

@author: Roberto
"""

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')
"""
TO NOTICE:
    sns.set_theme(style='darkgrid')
    https://github.com/mwaskom/seaborn/issues/2301
"""

df_meta = pd.read_csv('Indicators_metadata.csv', index_col='INDICATOR')
df_Big = pd.read_csv('gen_DF.csv', index_col=0)

sel_e = [#'Asset investment in renewables',
         #'Electricity Consumption',
         'Electricity generation',
         #'Electricity generation from other',
         #'Electricity Production',
         'Energy intensity-primary energy',
         #'Primary Energy-Consumption',
         'Renewables-Consumption Prim Energy',
         #'Renewable Energy Solar (Installed capacity)',
         #'Renewable Energy Wind  (Installed capacity)',
         #'Renewable installed PV Power',
         #'Renewable installed Wind Power',
         #'Renewable share electricity output',
         #'Renewable share electricity production',
         #'Renewable share energy of TFEC',
         #'Total electricity output',
         #'Total final energy consumption (TFEC)',
         #'Wind and solar share electricity production'
         ]

sel_f = [#'Government R&D',
         #'Corporate R&D',
         #'Venture capital',
         #'Private equity expansion capital',
         #'Public markets',
         #'Asset finance',
         'Asset Finance minus Re-invested equity',
         #'Small distributed capacity',
         #'Private equity buy-outs',
         #'Public markets investor exits',
         'Corporate M&A',
         #'Project acquisition & refinancing',
         #'Total: M&A/ buy-outs etc.',
         'Number of policies'
         ]

# Aggregate if wanted
#df_Big = df_Big.groupby('Year').mean()
#df_Big = df_Big.groupby('Year').sum()

# Proceed to plot
with sns.plotting_context("notebook", font_scale=2):
    for col_e in sel_e:
        for col_f in sel_f:
            # Adjust DF if necessary
            df_graph = df_Big
            # Set figure size (width, height) in inches 
            #fig, lm = plt.subplots(figsize = (15,6)) 
            df_graph[col_e] = df_graph[col_e] / df_graph[col_e].max()
            df_graph[col_f] = df_graph[col_f] / df_graph[col_f].max()
            # Plot the regplots
            lm = sns.lmplot(x=col_e, y=col_f, data=df_graph, hue='Country'
                            ,height=8.27, aspect=11.7/8.27, legend_out=False)
            # Save the figure
            plt.savefig(f"pair_plots/{col_f.replace(' ','_').replace('.','').replace('/','').replace(':','_')}_VS_{col_e}.jpg")#_Agg.jpg") 
            plt.close()