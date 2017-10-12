# coding: utf-8

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    f=open('university_towns.txt')
    lines=f.readlines()
    l=[]
    for line in lines:
        if ('[ed' in line):
            State=line.strip('\n').split("[")[0]
        else:
            RegionName=line.strip('\n').split(" (")[0]
            l.append([State,RegionName])
    df=pd.DataFrame(l,columns=["State", "RegionName"])
    return df


def get_GDP():
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
    df=get_GDP()
    flag=0
    for i in range(1,len(df)-4):
        if df.iloc[i,2]<0:
            flag+=1
        else:
            flag=0
        if flag>1 and df.iloc[i+1,2]<0:
            continue
        if flag>1 and df.iloc[i+1,2]>=0:
            pos=i-flag+1
    return df.iloc[pos,0]

	
def get_recession_end():
    df=get_GDP()
    for i in range(1,len(df)-4):
        target=df.iloc[i:i+4,2]
        target=target.tolist()
        if target==[-1,-1,1,1]:
            out=df.iloc[i+3,0]
    return out


def get_recession_bottom():
    df=get_GDP()
    for i in range(1,len(df)-4):
        target=df.iloc[i:i+4,2]
        target=target.tolist()
        if target==[-1,-1,1,1]:
            out=df.iloc[i+1,0]
    return out

	
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
    df=pd.read_csv('City_Zhvi_AllHomes.csv')
    tdf=df.iloc[:,51:252]
    tdf=tdf.T.rename(lambda x: pd.to_datetime(x))
    mdf=tdf.T.resample('Q',axis=1).mean()
    mdf=mdf.T.rename(lambda x: x.strftime('%Y-%m')).reset_index()
    mdf['index']=mdf.apply(quarter,axis=1)
    out=mdf.set_index('index').T
    out['State']=df['State']
    out['RegionName']=df['RegionName']
    out=out.set_index(["State","RegionName"])
    return out


re_states={v:k for k,v in states.items()}
def mapping(row):
    row['State']=re_states[row['State']]
    return row
def get_bstart(df,r_start):
    df=df.T
    for i,index in enumerate(df.index):
        if index==r_start:
            pos=i
    return df.index[pos-1]
def trending(row):
    row['change']=row[0]/row[2]
    return row
def run_ttest():
    uni_towns=get_list_of_university_towns().apply(mapping, axis=1)
    housing_data=convert_housing_data_to_quarters()
    r_start=get_recession_start()
    b_start=get_bstart(housing_data,r_start)
    r_bottom=get_recession_bottom()
    df=housing_data.T.loc[b_start:r_bottom]
    df=df.T.apply(trending, axis=1)
    
    subset=uni_towns[["State", "RegionName"]]
    tuple_list=[tuple(x) for x in subset.values]
    a=df.loc[tuple_list].dropna()['change']
    b=df.loc[~df.index.isin(tuple_list)].dropna()['change']
    t, p=ttest_ind(a,b)
    if p<0.01:
        different=True
    else:
        different=False
    u_mean=np.mean(a)
    n_mean=np.mean(b)
    if u_mean<n_mean:
        better="university town"
    else:
        better="non-university town"
    out=(different,p,better)
    return out

run_ttest()