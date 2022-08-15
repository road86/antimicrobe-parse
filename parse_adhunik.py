import re
import pandas as pd
import os

adhunik_data = os.path.join('..','input_data', 'unsorted', 'Raw AST data_ready to use', 'Uttara Adhumic Medical college, Dhaka_2021.xlsx')

adf = pd.read_excel(adhunik_data)
megagigalist = []

for iii, rrr in adf.iterrows():
    for abioind in range (0,76):
        anew_df = {
            'lab_id': rrr['Registration No.'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'specimen': rrr['Sample Type'],
            'pathogen': rrr['Growth Observation'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]

        }
        if anew_df['pathogen'] != 'No Growth':
             megagigalist.append(anew_df)
        if anew_df['pathogen'] != 'Mixed Growth':
             megagigalist.append(anew_df)
        if anew_df['pathogen'] != 'Due':
             megagigalist.append(anew_df)

outputloc = "outdata"

ast_data_adhunik = pd.DataFrame.from_records(megagigalist)
ast_data_adhunik.to_csv(f'{outputloc}/ast_data_adhunik.csv')