# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:23:31 2021

@author: danie
"""

import pandas as pd
import matplotlib.pyplot as plt

#function to convert all numbers to percentages of the total electricity
def convert_percentage(df):
    df_100 = df.copy()
    df_100 = pd.pivot_table(df_100,index=['country_or_area','year'],columns=['category'],values='quantity').fillna(0)
    df_100['total_electricity'] = df_100[list(df_100.columns)].sum(axis=1)
    df_100 = df_100.reset_index()
    for column in df_100.iloc[:,2:].columns:
        df_100.loc[:,column] = df_100.loc[:,column].div(df_100.iloc[:,-1])
    df_100 = df_100.melt(id_vars=['country_or_area','year'],value_vars=list(df_100.iloc[:,2:].columns),value_name='quantity')
    return df_100

#function to calculate the top x producing categories
def top_X(df,first_x,source=False,percentage=False):
    df_top_X = df.copy()
    df_top_X = df_top_X[df_top_X['unit']=='Kilowatt-hours, million']
    df_top_X = df_top_X[~df_top_X['category'].isin(['total_electricity','falling_water'])]
    if percentage == True:
        df_top_X = convert_percentage(df_top_X)
    if source != False:
        df_top_X = df_top_X[df_top_X['category'].isin([source])]
    df_top_X = df_top_X[df_top_X['year']==df_top_X['year'].max()][['country_or_area','quantity']].groupby('country_or_area').sum()
    df_top_X = df_top_X.sort_values(by='quantity', ascending=False).iloc[0:first_x].index
    key_countries = list(df_top_X)
    return key_countries

#function to produce a stacked bar chart of different data sources by year for a given country
def country_plot(df,country_selection,source=False,percentage=False):
    
    #setup data for stacked bar plot by year, return rows with kwh unit and not in total or falling water categories
    df_country = df.copy()
    df_country = df_country[df_country['unit']=='Kilowatt-hours, million']
    df_country = df_country[~df_country['category'].isin(['total_electricity','falling_water'])]
    if percentage == True:
        df_country = convert_percentage(df_country)
    if source != False:
        df_country = df_country[df_country['category'].isin([source])]        
    df_country = df_country[df_country['country_or_area']==country_selection][['year','category','quantity']]
    df_country_pivot = pd.pivot_table(df_country,index='year',columns='category',values='quantity')
    if 'total_electricity' in df_country_pivot.columns:
        df_country_pivot = df_country_pivot.drop(['total_electricity'],axis=1)

    #specify the colours of each of the differing sources
    colours = {'geothermal':'orange', 'hydro':'cyan', 'nuclear_electricity':'green',
                 'solar_electricity':'yellow', 'thermal_electricity':'red',
                 'tide_wave_and_ocean_electricity':'blue', 'wind_electricity':'purple'}

    #plot the stacked year data for your country
    plt.rcParams['figure.dpi'] = 150
    f,ax=plt.subplots(1,1,figsize=(16,5))
    df_country_pivot.plot(kind='bar',stacked=True,ax=ax,color=df_country_pivot.columns.map(colours))
    plt.title(country_selection)
