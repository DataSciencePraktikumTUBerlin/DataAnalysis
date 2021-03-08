# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:25:01 2021

@author: Roberto
"""

# Imports
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt


def deCumulate(cum_col, num_elem):
    '''
    Parameters
    ----------
    cum_col : panda Series
        Column, or series, to transform cummulative -> diff.
    num_elem : int
        Number of elements that repeat themselves in the series (index).

    Returns
    -------
    n_cumm_col : panda Series
        decumulated or differential column.
    '''
    cum_col = cum_col.reset_index(drop= True)
    n_cum_col = cum_col
    # Insert enough zeros per country selected, and erased last item
    for i in range(0, num_elem):
        cum_col = pd.concat([pd.Series([0]), cum_col])
        cum_col.pop(len(n_cum_col)-i-1)
    n_cum_col = n_cum_col - cum_col.array
    
    return n_cum_col

def robust_melt(df_melt, indic, col_1, col_2, group_sub = []):
    '''
    Parameters
    ----------
    df_melt : dataframe
        DF to be robustly melted.
    indic : string
        Name of the indicator in question.
    col_1 : string
        label of the primary column to use as ID_vars.
    col_2 : string
        label of next column, if exists.
    group_sub : list
        list of of column labels to use to group (in sum). The default is [].

    Returns 
    -------
    df_melt : dataframe
        melted DataFrame.
    '''
    df_col = list(df_melt.columns)
    if col_2 in df_col:
        melt_id = [col_1, col_2]
    else:
        melt_id = [col_1]
        
    df_melt=df_melt.melt(id_vars=melt_id)
    
    df_col = list(df_melt.columns)
    if col_2 in df_col:
        df_melt = df_melt.drop(labels = ['variable'],
                     axis=1, errors='ignore')
        df_melt = df_melt.rename(columns = {'value':indic})
    else:
        df_melt = df_melt.rename(columns = {'value': indic,
                                      'variable' : col_2})
    # Group subcategories per Year
    if (len(group_sub)>0):
        df_melt = df_melt.groupby(by=group_sub,as_index=False).sum()
    
    return df_melt


# Input Options
SELECTED_COUNTRIES = ['China', 'Germany', 'India', 'United States']
YEARS_INCLUDED = [2000,2016]
SOURCE_DIR = 'source_ult/'
EXCLUDE_SOURCE = ['web_ener_balance','web_indust_energinten','web_resid_energinten',
                  'web_serv_energinten','web_trans_energinten']

# Load all corresponding metadata in a compound dict (dict of dicts)
df_meta = pd.read_csv('Indicators_metadata_ult.csv').set_index('INDICATOR')

# Identify files to be preprocessed
csv_path_list = os.listdir(SOURCE_DIR)
csv_list = [file.replace('source_data/', '').replace('.csv', '') 
            for file in csv_path_list if file.split('.')[1]== 'csv' ]
for exc_item in EXCLUDE_SOURCE:
    csv_list.remove(exc_item)
    
# extract keys with which each file starts (one key == one source == one format)
df_keys = set(list(map(lambda f: f.split('_')[1], list(df_meta.KEY))))

# Adjust the DF to homogeneity
# Minimum requirements are a column for country Years (as colmns or variables)
df_dict_H = {}
for indic in df_meta.index :
    if not(df_meta['SPECIAL CASE'][indic]):
        df = pd.read_csv('source_ult/'+ df_meta['SOURCE FILE'][indic]+'.csv', index_col = 0)
        df_p = df.reset_index()
        
        # Changes to the Country Column
        df_p = df_p.rename(columns = {'Country Name':'Country'
                                      ,'Time' : 'Year' , 'Years' : 'Year'})
        df_p['Country'] = df_p['Country'].replace('US', 'United States')    
        
        # Selecting rows based on selected countries 
        df_p = df_p[df_p['Country'].isin(SELECTED_COUNTRIES)]
        
        # Drop unnecessary columns
        df_p = df_p.drop(labels = ['Country Code', 'Time Code', 'quarter'],
                         axis=1, errors='ignore')
        if (df_meta['KEY'][indic].split('_')[1] == 'A'):
            df_p = df_p[['Country', 'Year', indic]]            
        
        # Robust melting (contemplate different formats)
        df_p = robust_melt(df_p, indic, col_1 = 'Country', col_2 = 'Year'
                        , group_sub = ['Country', 'Year'])
        
        # Adjust column types
        df_p[indic]= pd.to_numeric(df_p[indic],errors='coerce')
        df_p['Year'] = pd.to_numeric(df_p['Year'],errors='coerce')
        
        # Selecting rows based on time range
        sel_y = YEARS_INCLUDED
        df_p = df_p[(df_p['Year']>=sel_y[0])&(df_p['Year']<=sel_y[1])]        
        df_p = df_p.sort_values(['Year', 'Country'], ascending=[True, True]) #sort for convenience
        df_p = df_p.reset_index(drop=True)
        
        # Operate over cumulative values
        if df_meta['CUMULATIVE'][indic]:
            df_p[indic] = deCumulate(df_p[indic], num_elem = len(SELECTED_COUNTRIES))
        
        # Save separated CSV and add to DF dictionary for plotting/merging
        df_p.to_csv(f"csv/new/{indic.replace(' ','_')}.csv")
        df_dict_H[indic] = df_p
        
# Proceed to plot
sns.set(context='talk', style='darkgrid')
for indic in df_meta.index:
    if not(df_meta['SPECIAL CASE'][indic]):
        # Adjust DF if necessary
        df_graph = df_dict_H[indic]
        df_graph['Year'] += 1 # values correspond to the END of every year (shift to the right)
        df_graph['Year'] = pd.to_datetime(df_graph['Year'] , format='%Y')
        # Set figure size (width, height) in inches 
        fig, ax = plt.subplots(figsize = ( 15 , 6 )) 
        # Plot the scatterplot 
        sns.lineplot(ax = ax , x='Year', y=indic, data=df_graph, hue='Country')
        # Set label for x-axis 
        ax.set_xlabel( 'Years' , size = 12 ) 
        # Set label for y-axis 
        ax.set_ylabel( df_meta['UNIT'][indic] , size = 12 ) 
        # Set title for plot 
        ax.set_title( indic , size = 24 ) 
        # Save the figure
        plt.savefig(f"csv/new/{indic.replace(' ','_')}.jpg")        
