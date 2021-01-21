#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:54:43 2020

@author: paul
"""

import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns


df0 = pd.read_csv('quaschning/windPower_00-02.csv')
df1 = pd.read_csv('quaschning/windPower_03-05.csv')
df2 = pd.read_csv('quaschning/windPower_06-08.csv')
df3 = pd.read_csv('quaschning/windPower_09-11.csv')
df4 = pd.read_csv('quaschning/windPower_12-14.csv')
df5 = pd.read_csv('quaschning/windPower_15-17.csv')
df6 = pd.read_csv('quaschning/windPower_18-20.csv')

all = pd.merge(df0, df1)
for frame in [df2, df3, df4, df5, df6]:
    all = pd.merge(all,frame, how='outer')
  
# replace NaN with 0    
all = all.fillna(0)

# select 2000-2019
all = all.drop(['2020'], axis = 1)

# restrict dec to 3
all = np.round(all, decimals=3)

# save as csv
all.to_csv('Wind_Power2000-2019.csv', index = True)


# make long
all_long = all.melt(['Land'])

# germany
all.set_index("Land", inplace = True)
Year = range(2000, 2020)
GW = all.loc['Deutschland'] 
data_plot1 = pd.DataFrame({"Year":Year, "GW":GW})
p1 = sns.lineplot(x = "Year", y = "GW", data=data_plot1)
p1.set_title('installed Wind Power in Germany')


# usa
GW = all.loc['USA'] 
data_plot2 = pd.DataFrame({"Year":Year, "GW":GW})
p2 = sns.lineplot(x = "Year", y = "GW", data=data_plot2)
p2.set_title('installed Wind Power in USA')


# china
GW = all.loc['China'] 
data_plot3 = pd.DataFrame({"Year":Year, "GW":GW})
p3 = sns.lineplot(x = "Year", y = "GW", data=data_plot3)
p3.set_title('installed Wind Power in China')


# usa
GW = all.loc['Indien'] 
data_plot4 = pd.DataFrame({"Year":Year, "GW":GW}) 
p4 = sns.lineplot(x = "Year", y = "GW", data=data_plot4)
p4.set_title('installed Wind Power in India')



# world average

# per capita ?? add population column to csv file 
