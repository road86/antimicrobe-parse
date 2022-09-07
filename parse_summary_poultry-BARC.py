import re
import pandas as pd
import os

barc_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'BARC 2018-2022.xlsx')


df = pd.read_excel(barc_data, header = [0])

##Checking
datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/barc.csv') #checking if skiprows and header give the desired result
##############

megagigalist = []

range_abio_columns = range(2, len(df.columns))

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind],
            'sensitive_isolates': rrr[rrr.index[abioind]]
        }
        megagigalist.append(new_df)

outputloc = "outdata"

ast_poultry = pd.DataFrame.from_records(megagigalist)
ast_poultry['sensitivity']=ast_poultry['sensitive_isolates']/ast_poultry['isolates_number']
ast_poultry['location']=pd.Series('unknown',index=ast_poultry.index)
ast_poultry['provider']=pd.Series('BARC',index=ast_poultry.index)

ast_poultry =  ast_poultry.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

ast_poultry.to_csv(f'{outputloc}/ast_poultry_BARC.csv')