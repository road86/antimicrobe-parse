import pandas as pd
import os

data_file = os.path.join('..','input_data','unsorted','AST data_ready to use','Khulna medical College_Jan 2021-Jul 2022-PATIENT_NAMES_REMOVED.xlsx')

df = pd.read_excel(data_file, header=[0,1,2])
corrected_cols = [x[1] for x in df.columns[0:7]] + [x[2] for x in df.columns[7:]]
df.columns = corrected_cols

ast_data = pd.melt(df,id_vars=df.columns[0:11], value_vars=df.columns[11:-3],var_name='antibiotic', value_name='sensitivity')

#there are two identical columns for each antibiotic, one has MIC result, another an interpretation
# we can get MIC from here later on

ast_data = ast_data[['Sl no', 'Date of enrollment', 'Age',
       'Specimen type', 'Identified bacteria',
       'antibiotic', 'sensitivity']]

ast_data.columns = ['lab_id', 'sample_date','sample_age', 'specimen', 'pathogen', 'antibiotic', 'sensitivity']

ast_data = ast_data[ast_data['sensitivity'].isin(['S','R','I','s'])]

ast_data['location']=pd.Series('khulna',index=ast_data.index)
ast_data['provider']=pd.Series('khulna-mc',index=ast_data.index)

ast_data.to_csv(os.path.join('outdata',f'ast_data_khulna-mc.csv'))
