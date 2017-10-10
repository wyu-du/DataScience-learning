# coding: utf-8


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def adjust_format(row):
    if ('[' in row[0]) and ('(' not in row[0]):
        row['State']=row[0].split("[")[0]
    if '(' in row[0]:
        row['RegionName']=row[0].split(" (")[0]
    return row

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df=pd.read_csv('university_towns.txt',sep='\n',header=None)
    df=df.apply(adjust_format, axis=1)
    df['State']=df['State'].fillna(method='ffill')
    df=df[df['RegionName'].notnull()]
    out=pd.DataFrame(df,columns=["State", "RegionName"])
    return out

get_list_of_university_towns()

def get_GDP():
    '''Returns a dataframe with columns=["time", "GDP", "trend"]'''
    df=pd.read_excel('gdplev.xls', parse_cols=[4, 6], skiprows=219, names=['time','GDP'])
    out=[]
    for i in range(len(df)):
        if i>0:
            if df.iloc[i-1,1]>df.iloc[i,1]:
                trend=-1
            if df.iloc[i-1,1]==df.iloc[i,1]:
                trend=0
            if df.iloc[i-1,1]<df.iloc[i,1]:
                trend=1
            out.append(trend)
        else:
            out.append("nan")
    df['trend']=out
    return df

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df=get_GDP()
    for i in range(1,len(df)-4):
        target=df.iloc[i:i+4,2]
        target=target.tolist()
        if target==[-1,-1,1,1]:
            out=df.iloc[i,0]
    return out

get_recession_start()

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df=get_GDP()
    for i in range(1,len(df)-4):
        target=df.iloc[i:i+4,2]
        target=target.tolist()
        if target==[-1,-1,1,1]:
            out=df.iloc[i+3,0]
    return out

get_recession_end()

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df=get_GDP()
    for i in range(1,len(df)-4):
        target=df.iloc[i:i+4,2]
        target=target.tolist()
        if target==[-1,-1,1,1]:
            out=df.iloc[i+1,0]
    return out

get_recession_bottom()

def quarter(row):
    index=str(row['index'])
    if index[5:]=='03':
        index=index[0:4]+"q1"
    if index[5:]=='06':
        index=index[0:4]+"q2"
    if index[5:]=='09':
        index=index[0:4]+"q3"
    if index[5:]=='12':
        index=index[0:4]+"q4"
    return index

def convert_housing_data_to_quarters():
    '''
    Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df=pd.read_csv('City_Zhvi_AllHomes.csv')
    tdf=df.iloc[:,51:204]
    tdf=tdf.T.rename(lambda x: pd.to_datetime(x))
    mdf=tdf.T.resample('Q',axis=1).mean()
    mdf=mdf.T.rename(lambda x: x.strftime('%Y-%m')).reset_index()
    mdf['index']=mdf.apply(quarter,axis=1)
    out=mdf.set_index('index').T
    out['State']=df['State']
    out['RegionName']=df['RegionName']
    out=out.set_index(["State","RegionName"])
    return out

convert_housing_data_to_quarters()