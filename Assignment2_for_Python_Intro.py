# coding: utf-8

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('
df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)
df = df.drop('Totals')
df.head()


def answer_one():
    max_medals=df[df['Gold']==max(df['Gold'])]
    country=max_medals.index
    return country[0]

def answer_two():
    df['gold_gap']=df['Gold']-df['Gold.1']
    max_gap=df.where(df['gold_gap']==max(df['gold_gap'])).dropna()
    country2=max_gap.index
    return country2[0]

def answer_three():
    df_copy=df[(df['Gold']>0) & (df['Gold.1']>0)].dropna()
    df_copy['ave_gap']=(df_copy['Gold']-df_copy['Gold.1'])/(df_copy['Gold']+df_copy['Gold.1'])
    maxave_gap=df_copy[df_copy['ave_gap']==max(df_copy['ave_gap'])]
    country3=maxave_gap.index
    return country3[0]

def answer_four():
    Points=pd.Series(df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2']*1)
    return Points


	
census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    census=census_df[census_df['SUMLEV']==50]
    census=census.set_index('STNAME')
    state={}
    for a in census.index:
        if a not in state:
            state[a]=1
        else:
            state[a]+=1
    census['CNUMS']=pd.Series(state)
    max_cnums=census[census['CNUMS']==max(census['CNUMS'])].dropna()
    output=max_cnums.index
    return output[0]

def answer_six():
    census=census_df[census_df['SUMLEV']==50]
    census=census.set_index(['STNAME','CTYNAME'])
    state={}
    for a in census.index:
        state[a]=census.loc[a,'CENSUS2010POP']
    # 对字典的value进行排序：把字典转化成list或者tuple，把字典每一对键值转化为list中的两位子list或者子tuple再输出
    # items()返回字典键值对的元祖集合
    sorted_state=sorted(state.items(), key=lambda d:d[1], reverse=True)
    state2={}
    for keys in sorted_state:
        if(keys[0][0] not in state2):
            state2.setdefault(keys[0][0],[]).append(keys[1])
            state2.setdefault(keys[0][0],[]).append(0)
        elif((keys[0][0] in state2) & (state2[keys[0][0]][1]<2)):
            state2[keys[0][0]][0]+=keys[1]
            state2[keys[0][0]][1]+=1
    state3={}
    for key in state2:
        state3[key]=state2[key][0]
    sorted_state2=sorted(state3.items(),key=lambda d:d[1], reverse=True)
    output=[]
    for i,sname in enumerate(sorted_state2):
        if i<3:
            output.append(sname[0])
    return output

def answer_seven():
    census=census_df[census_df['SUMLEV']==50]
    census=census.set_index('CTYNAME')
    county={}
    for a in census.index:
        pop=[]
        for i in range(6):
            year='POPESTIMATE201'+str(i)
            if(type(census.loc[a,year])!='numpy.int64'):
                pop.append(census.loc[a,year].sum())
            else:
                pop.append(census.loc[a,year])
        change=abs(max(pop)-min(pop))
        county[a]=change
    sorted_county=sorted(county.items(), key=lambda d:d[1], reverse=True)
    return sorted_county[0][0]

def answer_eight():
    census=census_df[census_df['SUMLEV']==50]
    census=census[(census['REGION']==1)|(census['REGION']==2)]
    census['ID']=census.index
    output=pd.DataFrame(columns = ['STNAME', 'CTYNAME'])
    for a in census.index:
        if(census.loc[a,'CTYNAME'][0:10]=='Washington'):
            if(census.loc[a,'POPESTIMATE2015']>census.loc[a,'POPESTIMATE2014']):
                output.loc[census.loc[a,'ID']]={'STNAME':census.loc[a,'STNAME'],'CTYNAME':census.loc[a,'CTYNAME']}
    return output


