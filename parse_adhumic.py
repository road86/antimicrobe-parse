import re
import pandas as pd
import os

adhunik_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'Uttara Adhumic Medical college, Dhaka_2021.xlsx')

df = pd.read_excel(adhunik_data, header=[0,1,2]) #first three lines a header
corrected_cols = [x[1] for x in df.columns[0:11]] + [x[2] for x in df.columns[11:]]
df.columns = corrected_cols
range_abio_columns = range(11, len(df.columns))

megagigalist = []

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        anew_df = {
            'lab_id': rrr['Registration No.'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'sample_date': rrr['Date of Case Enrolment'],
            'specimen': rrr['Sample Type'],
            'pathogen': rrr['Growth Observation'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]

        }

        if not anew_df['pathogen'] in ['No Growth', 'Mixed Growth', 'Due']:
             megagigalist.append(anew_df)

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

outputloc = "outdata"


ast_data['location']=pd.Series('dhaka',index=ast_data.index)
ast_data['provider']=pd.Series('adhumic',index=ast_data.index)

ast_data.to_csv(f'{outputloc}/ast_data_adhumic.csv')
