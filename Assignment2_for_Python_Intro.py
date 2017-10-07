# coding: utf-8


# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.
# 

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


# ### Question 1
# Which country has won the most gold medals in summer games?
# 

def answer_one():
    max_medals=df[df['Gold']==max(df['Gold'])]
    country=max_medals.index
    return country[0]

answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 

def answer_two():
    df['gold_gap']=df['Gold']-df['Gold.1']
    max_gap=df.where(df['gold_gap']==max(df['gold_gap'])).dropna()
    country2=max_gap.index
    return country2[0]

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 

def answer_three():
    df_copy=df[(df['Gold']>0) & (df['Gold.1']>0)].dropna()
    df_copy['ave_gap']=(df_copy['Gold']-df_copy['Gold.1'])/(df_copy['Gold']+df_copy['Gold.1'])
    maxave_gap=df_copy[df_copy['ave_gap']==max(df_copy['ave_gap'])]
    country3=maxave_gap.index
    return country3[0]

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 

def answer_four():
    Points=pd.Series(df['Gold.2']*3+df['Silver.2']*2+df['Bronze.2']*1)
    return Points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 

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

answer_five()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 

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

answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 

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

answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 

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

answer_eight()

