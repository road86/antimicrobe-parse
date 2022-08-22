import re
import pandas as pd
import os

ibhdhaka_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'Islami bank hospital, Dhaka_2021.xlsx')

df = pd.read_excel(ibhdhaka_data, skiprows = 2, header = [3]) #skipping non-data info on top and defining the header

os.makedirs('check', exist_ok=True)
datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/check.csv') #checking if skiprows and header give the desired result

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

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data['sensitivity']=ast_data['sensitive_isolates']/ast_data['isolates_number']
ast_data['specimen']=pd.Series('Urine',index=ast_data.index)
ast_data['location']=pd.Series('dhaka',index=ast_data.index)
ast_data['provider']=pd.Series('islamic bank hospital',index=ast_data.index)


ast_data.to_csv(f'{outputloc}/ast_data_ibhdhaka.csv')
