import re
import pandas as pd
import os

birdem_data = os.path.join('..','input_data', 'unsorted', 'Raw AST data_ready to use', 'BIRDEM Hospital_2021.xlsx')

df = pd.read_excel(birdem_data)
megagigalist = []



for iii, rrr in df.iterrows():
    for abioind in range (0,76):
        new_df = {
            'lab_id': rrr['Lab ID'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'specimen': rrr['Sample Name'],
            'pathogen': rrr['Organism Name'],
            'observation': rrr['Observation'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]
        }
        if new_df['observation'] != 'No Growth':
             megagigalist.append(new_df)

outputloc = "outdata"

ast_data_birdem = pd.DataFrame.from_records(megagigalist)
ast_data_birdem.to_csv(f'{outputloc}/ast_data_birdem.csv')