# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:12:41 2021

@author: Roberto
"""

# Imports
import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt

# Input Options
SELECTED_COUNTRIES = ['China', 'Germany', 'India', 'United States']
YEARS_INCLUDED = [2000,2018]

# Load all corresponding metadata in a compound dict (dict of dicts)
df_meta = pd.read_csv('Indicators_metadata.csv')
df_meta_temp = df_meta.set_index('KEY')

# Identify files to be preprocessed
csv_path_list = glob.glob('source_data/Energy/*.csv', recursive=True)
csv_list = [file.replace('source_data/Energy\\', '').replace('.csv', '') for file in csv_path_list]

# Build the Dict
df_metadict={}
for ind_key in df_meta['KEY']:
#    if df_meta_temp['SOURCE FILE'][ind_key] in csv_list:
    df_metadict_sub = {}
    df_metadict_sub['Units_ind']= df_meta_temp['UNIT'][ind_key]
    df_metadict_sub['Origin_ind']= df_meta_temp['SITE'][ind_key]
    df_metadict_sub['Name_ind'] =  df_meta_temp['INDICATOR'][ind_key]
    df_metadict_sub['Desc_ind'] =  df_meta_temp['DESCRIPTION'][ind_key]
    df_metadict_sub['source_file'] =  df_meta_temp['SOURCE FILE'][ind_key]+'.csv'
    df_metadict_sub['excep_format'] = df_meta_temp['SPECIAL FORMAT'][ind_key]
    df_metadict[ind_key] = df_metadict_sub 

indicators=list(df_metadict.keys())        

# Call desired data and stored in DF-Dict
df_dict = {}
for indic in indicators:    
    df_dict[indic] = pd.read_csv('source_data/Energy\\'+ df_metadict[indic]['source_file'])
    
# Include manual selection of indicators when needed
indicators= [
 'ASST_D'
]

# Adjust the DF to homogeneity
df_dict_H = {}
for indic in indicators:    
        Name_ind =df_metadict[indic]['Name_ind']
        df_p = df_dict[indic]
        # Melt to a Long format
        df_p=df_dict[indic].melt(id_vars=['Country','Years'])
        # Rename column to Years
        #df_p =df_p.rename(columns = {'variable':'Years'})
        # Delete columns with NaN values (in any Column)
        df_p.dropna(inplace = True)
        # Adjust column types
        df_p['value']= pd.to_numeric(df_p['value'],errors='coerce')
        df_p['Years'] = pd.to_numeric(df_p['Years'],errors='coerce')
        # Rename column to Indic Name
        df_p =df_p.rename(columns = {'value':Name_ind})
        # group subcategories of Indicator
        df_p = df_p.groupby(by=['Country', 'Years'],as_index=False).mean()        
        # Selecting rows based on time range and selected countries 
        sel_y = YEARS_INCLUDED
        df_p =df_p[(df_p['Years']>=sel_y[0])&(df_p['Years']<=sel_y[1])]
        df_p = df_p[df_p.Country.isin(SELECTED_COUNTRIES)]
        # Clean the indexes
        df_p = df_p.set_index('Country')
        df_p = df_p.reset_index()
        df_p.to_csv('No_Notebook/On_test/' + Name_ind +'.csv')
        df_dict_H[indic] = df_p 

# Proceed to plot
sns.set(context='talk', style='darkgrid')
for indic in indicators:
    # Adjust DF if necessary
    df_graph = df_dict_H[indic]
    df_graph['Years'] += 1 # values correspond to the END of every year (shift to the right)
    df_graph['Years'] = pd.to_datetime(df_graph['Years'] , format='%Y')
    # Set figure size (width, height) in inches 
    fig, ax = plt.subplots(figsize = ( 15 , 6 )) 
    # Plot the scatterplot 
    sns.lineplot(ax = ax , x='Years', y=df_metadict[indic]['Name_ind'], data=df_graph, hue='Country')
    # Set label for x-axis 
    ax.set_xlabel( 'Years' , size = 12 ) 
    # Set label for y-axis 
    ax.set_ylabel( df_metadict[indic]['Units_ind'] , size = 12 ) 
    # Set title for plot 
    ax.set_title( df_metadict[indic]['Name_ind'] , size = 24 ) 
    # Save the figure
    plt.savefig('No_Notebook/On_test/' + df_metadict[indic]['Name_ind'] +'.jpg')
    # Display figure 
    plt.show() 