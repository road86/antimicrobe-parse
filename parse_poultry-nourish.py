import uuid
import re
import pandas as pd
import os

nourish_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'Antibiotic Sensitivity Report@ 20.08.22.xlsx')


df1 = pd.read_excel(nourish_data, sheet_name = 'E.Coli', skiprows = 3, nrows= 25, header = [4])
df2 = pd.read_excel(nourish_data, sheet_name = 'Staphylococcus', skiprows = 3, nrows= 23, header = [4])
df3 = pd.read_excel(nourish_data, sheet_name = 'Pseudomonas', skiprows = 3, nrows= 25, header = [4])

##checking
datacheck = 'check' # folder to store script checks
df1.to_csv(f'{datacheck}/nourish1.csv') #checking if skiprows and header give the desired result
df2.to_csv(f'{datacheck}/nourish2.csv')
df3.to_csv(f'{datacheck}/nourish3.csv')
##################

#for each antibiotic result there is a columns
abio_columns_1 = range(3, len(df1.columns))
abio_columns_2 = range(3, len(df2.columns))
abio_columns_3 = range(3, len(df3.columns))

megagigalist = []

# for E. coli
for iii, rrr in df1.iterrows():
    for abioind1 in abio_columns_1:
        new_df1 = {
            'pathogen': rrr['Name of pathogen'],
            'antibiotic': rrr.index[abioind1],
            'sensitivity': rrr[rrr.index[abioind1]]
        }
        new_df1['Isolates']=25
        megagigalist.append(new_df1)

# for Staphylococcus
for iii, rrr in df2.iterrows():
    for abioind2 in abio_columns_2:
        new_df2 = {
            'pathogen': rrr['Name of pathogen'],
            'antibiotic': rrr.index[abioind2],
            'sensitivity': rrr[rrr.index[abioind2]]
        }
        new_df2['Isolates']=23
        megagigalist.append(new_df2)

# for
for iii, rrr in df3.iterrows():
    for abioind3 in abio_columns_3:
        new_df3 = {
            'pathogen': rrr['Name of pathogen'],
            'antibiotic': rrr.index[abioind3],
            'sensitivity': rrr[rrr.index[abioind3]]
        }
        new_df3['Isolates']=25
        megagigalist.append(new_df3)


outputloc = "outdata"

poultry_data = pd.DataFrame.from_records(megagigalist)
poultry_data = poultry_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

