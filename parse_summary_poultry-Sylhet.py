import re
import pandas as pd
import os

sylhet_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'Sylhet.xlsx')


df = pd.read_excel(sylhet_data, header = [0])

##Checking
datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/sylhet_poultry.csv') #checking if skiprows and header give the desired result
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
ast_poultry['location']=pd.Series('Sylhet',index=ast_poultry.index)
ast_poultry['provider']=pd.Series('unknown',index=ast_poultry.index)

ast_poultry =  ast_poultry.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

ast_poultry.to_csv(f'{outputloc}/ast_poultry_sylhet.csv')
