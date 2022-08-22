import re
import pandas as pd
import os

aftab_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'AST data for FAO (for the year 2021-22)_ 17.08.22.xlsx')


df = pd.read_excel(aftab_data, header = [0])

##Checking
datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/poultry.csv') #checking if skiprows and header give the desired result
##############

megagigalist = []

range_abio_columns = range(2, len(df.columns))

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'pathogen': rrr['Name of pathogen'],
            'isolates_number': rrr['Total number of isolates'],
            'antibiotic': rrr.index[abioind],
            'sensitive_isolates': rrr[rrr.index[abioind]]
        }
        megagigalist.append(new_df)

outputloc = "outdata"

ast_poultry = pd.DataFrame.from_records(megagigalist)
ast_poultry['sensitivity']=ast_poultry['sensitive_isolates']/ast_poultry['isolates_number']
ast_poultry['location']=pd.Series('dhaka',index=ast_poultry.index)
ast_poultry['provider']=pd.Series('Aftab',index=ast_poultry.index)

ast_poultry.to_csv(f'{outputloc}/ast_poultry_aftab.csv')