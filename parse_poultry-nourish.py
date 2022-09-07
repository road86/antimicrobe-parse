import uuid
import re
import pandas as pd
import os

nourish_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'Antibiotic Sensitivity Report@ 20.08.22.xlsx')

#from the header (niso = int(df1.columns[2].split('(')[1].split(')')[0])) we can red how many rows are needed
df0 = pd.read_excel(nourish_data, sheet_name = 'E.Coli', skiprows = 3, nrows= 25, header = [4])
df2 = pd.read_excel(nourish_data, sheet_name = 'Staphylococcus', skiprows = 3, nrows= 23, header = [4])
df3 = pd.read_excel(nourish_data, sheet_name = 'Pseudomonas', skiprows = 3, nrows= 25, header = [4])

##checking
datacheck = 'check' # folder to store script checks
df0.to_csv(f'{datacheck}/nourish1.csv') #checking if skiprows and header give the desired result
df2.to_csv(f'{datacheck}/nourish2.csv')
df3.to_csv(f'{datacheck}/nourish3.csv')
##################


preped_frames = []

for df1 in [df0, df2, df3]:
    ecoli = pd.melt(df1,id_vars=df1.columns[0:3], value_vars=df1.columns[3:],var_name='antibiotic', value_name='sensitivity')
    ecoli.columns = ['serial','pathogen','skip','antibiotic','sensitivity']
    ecoli2 = ecoli.groupby(['pathogen','antibiotic','sensitivity'])['serial'].count().reset_index()

    ecoli3 = pd.pivot(ecoli2, index=['pathogen','antibiotic'], columns='sensitivity', values='serial').reset_index().fillna(0)

    ecoli3['sensitivity'] = ecoli3.apply(lambda x: x['R']/(x['NR']+x['R']),axis=1)
    ecoli3 = ecoli3[['pathogen', 'antibiotic', 'R', 'sensitivity']]
    ecoli3.columns = ['pathogen', 'antibiotic', 'sensitive_isolates', 'sensitivity']

    niso = int(df1.columns[2].split('(')[1].split(')')[0])

    ecoli3['isolates_number']=pd.Series(niso,index=ecoli3.index)
    ecoli3['location']=pd.Series('unkown',index=ecoli3.index)
    ecoli3['provider']=pd.Series('Nourish',index=ecoli3.index)
    preped_frames.append(ecoli3)

poultry_data = pd.concat(preped_frames)

outputloc = "outdata"

poultry_data = poultry_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

poultry_data.to_csv(f'{outputloc}/ast_poultry_nourish.csv')
