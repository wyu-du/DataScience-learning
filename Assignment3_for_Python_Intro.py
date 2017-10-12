# coding: utf-8

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

	
def avgGDP(row):
    data=row[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    row['avgGDP']=np.mean(data)
    return row
def answer_three():
    Top15 = answer_one()
    output=Top15.apply(avgGDP, axis=1)
    output=output.sort_values(by='avgGDP',ascending=False)
    return output['avgGDP']

	
def answer_four():
    Top15 = answer_one()
    output=Top15.loc['United Kingdom','2015']-Top15.loc['United Kingdom','2006']
    return output

	
def answer_five():
    Top15 = answer_one()
    output=np.mean(Top15['Energy Supply per Capita'])
    return output

	
def answer_six():
    Top15 = answer_one()
    country_list=Top15.sort_values(by='% Renewable',ascending=False)
    country=country_list.index[0]
    percentage=country_list.loc[country,'% Renewable']
    output=(country,percentage)
    return output

	
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

	
def population(row):
    row['population']=row['Energy Supply']/row['Energy Supply per Capita']
    return row
def answer_eight():
    Top15 = answer_one()
    Top15=Top15.apply(population, axis=1).sort_values(by='population',ascending=False)
    country=Top15.index[2]
    return country

	
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

	
def transtype(row):
    row['PopEst']=format(row['population'],',')
    return row
def answer_thirteen():
    Top15 = answer_one()
    Top15=Top15.apply(population, axis=1)
    output=Top15.apply(transtype, axis=1)['PopEst']
    return output
