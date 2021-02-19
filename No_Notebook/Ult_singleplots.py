# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 20:41:07 2021

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

df_meta = pd.read_csv('Indicators_metadata_ult.csv', index_col='INDICATOR')
df_Big = pd.read_csv('Big_DF.csv', index_col=0)

# Proceed to plot
for col in df_Big.columns:
    if col in ['Country', 'Year']:
        continue
    
    # Adjust DF if necessary
    df_graph = df_Big
    #df_graph['Years'] += 1 # values correspond to the END of every year (shift to the right)
    df_graph['Year'] = pd.to_datetime(df_graph['Year'] , format='%Y')
    # Set figure size (width, height) in inches 
    fig, ax = plt.subplots(figsize = ( 15 , 6 )) 
    # Plot the scatterplot 
    sns.lineplot(ax = ax , x='Year', y=col, data=df_graph, hue='Country')
    # Set label for x-axis 
    ax.set_xlabel( 'Year' , size = 12 ) 
    # Set label for y-axis 
    if col in df_meta.index:
        ax.set_ylabel( df_meta['UNIT'][col] , size = 12 ) 
    # Set title for plot 
    ax.set_title( col , size = 24 ) 
    # Save the figure
    if col in df_meta.index:
        plt.savefig(f"Plots_grouped/from_BigDF/En-{col.replace(' ','_')}.jpg")
    else:
        plt.savefig(f"Plots_grouped/from_BigDF/Fin-{col.replace(' ','_').replace('.','').replace('/','').replace(':','_')}.jpg")
    # Display figure 
 #   plt.show() 