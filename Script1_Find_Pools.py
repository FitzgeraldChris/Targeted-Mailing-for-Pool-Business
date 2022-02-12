# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 16:56:01 2021

@author: chris
"""

import pandas as pd

# Check if report has ground pool

df = pd.read_excel('placer_county.xlsx')
# Remove location with no addresses from file
df = df[(df.FULLSTREET.notnull()) and (df.FULLSTREET != 'NO ADDRESS ON FILE')]
#Focus on two major areas
df = df[(df.ZIP == '95661') | (df.ZIP == '95765')]

print(df.CityName.unique())
print(df.CityName.value_counts())
print(df.ZIP.value_counts())

mailing_address = pd.DataFrame()

count = 0
#Check through the dataframe for any 
for i in range(len(df)):
    try:
        table_county = pd.read_html(df.loc[i,"Assessment"])
        individ_df = table_county[0]
        individ_df.rename(columns={0 :'Object'}, inplace=True)
        if pd.notnull(individ_df.iat[42,1]):
            print(individ_df.iat[42,1])
            print("This has a pool!")
            print(df.iat[i,0])
            ls = [df.iat[i,0], df.iat[i,1], df.iat[i,3], individ_df.iat[42,1]]
            new_row = pd.Series(ls)
            mailing_address = mailing_address.append(new_row, ignore_index=True)
            count += 1
    except: pass    
print("Now the count is")   
print(count)
mailing_address = mailing_address.rename(columns={0:"FULL STREET",1: "ZIP", 2: "City", 3: "Pool Type"})

#Does not want any vinyl pools
mailing_address[mailing_address.PoolType != 'V']

#Export the desired addresses to csv
gfg_csv_data = mailing_address.to_csv('TargetedMailingADD.csv', index = False)
# a /
# h / hot tub/spa
# v / vinyl pool
# s / hot tub/spa
# g / groud pool