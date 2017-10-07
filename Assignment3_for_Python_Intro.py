# coding: utf-8


# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].


import pandas as pd
import numpy as np 
import re

def convert_country(row):
    row['Country']=re.sub(r'[\d]','',row['Country'])
    if "(" in row['Country']:
        row['Country']=row['Country'].split(" (")[0]
    if row['Country']=="Republic of Korea":
        row['Country']="South Korea"
    if row['Country']=="United States of America":
        row['Country']="United States"
    if row['Country']=="United Kingdom of Great Britain and Northern Ireland": 
        row['Country']="United Kingdom"
    if row['Country']=="China, Hong Kong Special Administrative Region": 
        row['Country']="Hong Kong"
    return row['Country']

def rename_country(row):
    if row['Country Name']=="Korea, Rep.":
        row['Country Name']="South Korea"
    if row['Country Name']=="Iran, Islamic Rep.":
        row['Country Name']="Iran"
    if row['Country Name']=="Hong Kong SAR, China": 
        row['Country Name']="Hong Kong"
    return row['Country Name']

def answer_one():
    energy=pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38, parse_cols=[2,3,4,5], 
                         names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],
                         na_values=["..."])
    energy['Energy Supply']=1000000*energy['Energy Supply']
    energy['Country']=energy.apply(convert_country, axis=1)
    
    GDP=pd.read_csv('world_bank.csv',skiprows=4, usecols=['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'])
    GDP['Country Name']=GDP.apply(rename_country, axis=1)
    ScimEn=pd.read_excel('scimagojr-3.xlsx')
    
    energy=energy.set_index('Country')
    GDP=GDP.set_index('Country Name')
    ScimEn=ScimEn.set_index('Country')
    t1=pd.merge(ScimEn, energy, how='outer', left_index=True, right_index=True)
    t2=pd.merge(t1, GDP, how='outer', left_index=True, right_index=True)
    
    output=t2[t2['Rank']<16]
    output[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'H index']]=output[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'H index']].astype('Int64')
    return output

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?


def answer_two():
    #items lost = len(union of all three df) - len(intersection of all 3 df)
    energy=pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38, parse_cols=[2,3,4,5], 
                         names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],
                         na_values=["..."])
    energy['Energy Supply']=1000000*energy['Energy Supply']
    energy['Country']=energy.apply(convert_country, axis=1)
    GDP=pd.read_csv('world_bank.csv',skiprows=4, usecols=['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'])
    GDP['Country Name']=GDP.apply(rename_country, axis=1)
    ScimEn=pd.read_excel('scimagojr-3.xlsx')
    
    energy=energy.set_index('Country')
    GDP=GDP.set_index('Country Name')
    ScimEn=ScimEn.set_index('Country')
    t1=pd.merge(ScimEn, energy, how='outer', left_index=True, right_index=True)
    t2=pd.merge(t1, GDP, how='outer', left_index=True, right_index=True)
    t3=pd.merge(ScimEn, energy, how='inner', left_index=True, right_index=True)
    t4=pd.merge(t3, GDP, how='inner', left_index=True, right_index=True)
    output=len(t2)-len(t4)
    return output

answer_two()


# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
#

def avgGDP(row):
    data=row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    row['avgGDP']=np.mean(data)
    return row

def answer_three():
    Top15 = answer_one()
    output=Top15.apply(avgGDP, axis=1)
    output=output.sort_values(by='avgGDP',ascending=False)
    return output['avgGDP']

answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 

def answer_four():
    Top15 = answer_one()
    output=Top15.loc['United Kingdom','2015']-Top15.loc['United Kingdom','2006']
    return output

answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 

def answer_five():
    Top15 = answer_one()
    output=np.mean(Top15['Energy Supply per Capita'])
    return output

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 

def answer_six():
    Top15 = answer_one()
    country_list=Top15.sort_values(by='% Renewable',ascending=False)
    country=country_list.index[0]
    percentage=country_list.loc[country,'% Renewable']
    output=(country,percentage)
    return output

answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 

def ratio(row):
    row['ratio']=row['Self-citations']/row['Citations']
    return row

def answer_seven():
    Top15 = answer_one()
    Top15=Top15.apply(ratio, axis=1)
    ranking=Top15.sort_values(by='ratio', ascending=False)
    country=ranking.index[0]
    value=ranking.iloc[0,20]
    output=(country,value)
    return output

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 

def population(row):
    row['population']=row['Energy Supply']/row['Energy Supply per Capita']
    return row

def answer_eight():
    Top15 = answer_one()
    Top15=Top15.apply(population, axis=1).sort_values(by='population',ascending=False)
    country=Top15.index[2]
    return country

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
#  

def DC_per(row):
    row['Citable documents per capita']=row['Citable documents']/row['population']
    return row

def answer_nine():
    Top15 = answer_one()
    Top15=Top15.apply(population, axis=1)
    Top15=Top15.apply(DC_per, axis=1)
    corr=Top15.corr(method ='pearson')
    output=corr.loc['Citable documents per capita','Energy Supply per Capita']
    return output

answer_nine()


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 

def discrimintate(data, median):
    if data<median:
        data=0
    else:
        data=1
    return data

def answer_ten():
    Top15 = answer_one()
    median=Top15['% Renewable'].median()
    Top15['HighRenew']=Top15.apply(lambda x: discrimintate(x['% Renewable'],median), axis=1)
    HighRenew=Top15.sort_values(by='Rank', ascending=True)['HighRenew']
    return HighRenew

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 

def groupBycontinent(row):
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    row['Continent']=ContinentDict[row[0]]
    return row

def answer_eleven():
    Top15 = answer_one()
    Top15=Top15.reset_index()
    Top15=Top15.apply(population, axis=1)
    Top15=Top15.apply(groupBycontinent, axis=1)
    df=pd.DataFrame(columns=['size', 'sum', 'mean', 'std'])
    for continent,frame in Top15.groupby('Continent'):
        df.loc[continent,'size']=len(frame)
        df.loc[continent,'sum']=np.sum(frame['population'])
        df.loc[continent,'mean']=np.mean(frame['population'])
        df.loc[continent,'std']=np.std(frame['population'])
    return df.astype('float64')

answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 

def answer_twelve():
    Top15 = answer_one()
    Top15=Top15.reset_index()
    Top15=Top15.apply(groupBycontinent, axis=1)
    Top15['Bins']=pd.cut(Top15['% Renewable'],5)
    Top15['Bins']=pd.Categorical(list(Top15['Bins']),
                     categories=sorted(list(Top15['Bins'].cat.categories)),
                     ordered=True)
    # select a column 'Continent' and use agg to calculate the number of entries in each group
    output=Top15.groupby(['Continent','Bins'])['Continent'].agg(len)
    return output

answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 

def transtype(row):
    row['PopEst']=format(row['population'],',')
    return row

def answer_thirteen():
    Top15 = answer_one()
    Top15=Top15.apply(population, axis=1)
    output=Top15.apply(transtype, axis=1)['PopEst']
    return output

answer_thirteen()
