import re
import pandas as pd
import os

birdem_data = os.path.join('data', 'amr_guidline_revision', 'unsorted', 'RAW AST data_ready to use', 'BIRDEM Hospital_2021.xlsx')

df = pd.read_excel(birdem_data)
megagigalist = []

for iii, rrr in df.iterrows():
    for abioind in range (0,72):
        new_df = {
            'lab_id': rrr['Lab ID'],
            'patient_name': rrr['Patient Name'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'specimen': rrr['Sample Name'],
            'pathogen': rrr['Organism Name'],
            'observation': rrr['Observation'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]
        }

        new_df[new_df.observation != 'No Growth']
        megagigalist.append(new_df)

outputloc = "outdata"

ast_data_birdem = pd.DataFrame.from_records(megagigalist)
ast_data_birdem.to_csv(f'{outputloc}/ast_data_birdem.csv')