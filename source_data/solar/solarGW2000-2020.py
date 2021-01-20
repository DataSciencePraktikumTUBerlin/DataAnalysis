#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 12:49:46 2020

@author: paul
"""
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns


df0 = pd.read_csv('gw welt quaschning/pvPower_01-03.csv')
df1 = pd.read_csv('gw welt quaschning/pvPower_04-06.csv')
df2 = pd.read_csv('gw welt quaschning/pvPower_07-09.csv')
df3 = pd.read_csv('gw welt quaschning/pvPower_10-12.csv')
df4 = pd.read_csv('gw welt quaschning/pvPower_13-15.csv')
df5 = pd.read_csv('gw welt quaschning/pvPower_16-18.csv')
df6 = pd.read_csv('gw welt quaschning/pvPower_19-21.csv')
df7 = pd.read_csv('gw welt quaschning/pvPower_98-00.csv')

all = pd.merge(df7, df0)
for frame in [df1, df2, df3, df4, df5, df6]:
    all = pd.merge(all,frame, how='outer')
  
# replace NaN with 0    
all = all.fillna(0)

# select 2000-2019
all = all.drop(['1998', '1999', '2020', '2021'], axis = 1)

# bring 2000-2006 from MW to GW
all.update(all.iloc[:, 1:8].div(1000))

# restrict dec to 3
all = np.round(all, decimals=3)

# save as csv
all.to_csv('Solar_PV_Power2000-2019.csv', index = True)


# make long
all_long = all.melt(['Land'])

# germany
all.set_index("Land", inplace = True)
Year = range(2000, 2020)
GW = all.loc['Deutschland'] 
data_plot1 = pd.DataFrame({"Year":Year, "GW":GW})
p1 = sns.lineplot(x = "Year", y = "GW", data=data_plot1)
p1.set_title('installed PV Power in Germany')


# usa
GW = all.loc['USA'] 
data_plot2 = pd.DataFrame({"Year":Year, "GW":GW})
p2 = sns.lineplot(x = "Year", y = "GW", data=data_plot2)
p2.set_title('installed PV Power in USA')


# china
GW = all.loc['China'] 
data_plot3 = pd.DataFrame({"Year":Year, "GW":GW})
p3 = sns.lineplot(x = "Year", y = "GW", data=data_plot3)
p3.set_title('installed PV Power in China')


# usa
GW = all.loc['Indien'] 
data_plot4 = pd.DataFrame({"Year":Year, "GW":GW}) 
p4 = sns.lineplot(x = "Year", y = "GW", data=data_plot4)
p4.set_title('installed PV Power in India')


# world average

# per capita ?? add population column to csv file 