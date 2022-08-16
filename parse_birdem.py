import re
import pandas as pd
import os

birdem_data = os.path.join('..','input_data', 'unsorted', 'Raw AST data_ready to use', 'BIRDEM Hospital_2021.xlsx')

df = pd.read_excel(birdem_data)
megagigalist = []


#for each antibiotic result there is a columns
range_abio_columns = range(22, len(df.columns))

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'lab_id': rrr['Lab ID'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'sample_date': rrr['MR Receiving Date'],
            'specimen': rrr['Sample Name'],
            'pathogen': rrr['Organism Name'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]
        }
        if rrr['Observation'] != 'No Growth':
             megagigalist.append(new_df)

outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data = ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

ast_data['location']=pd.Series('dhaka',index=ast_data.index)
ast_data['provider']=pd.Series('birdem',index=ast_data.index)

ast_data.to_csv(f'{outputloc}/ast_data_birdem.csv')
