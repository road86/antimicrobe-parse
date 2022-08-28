import re
import pandas as pd
import os


cdil_code = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'AST-Results_analysis (CDIL).xlsx')

df = pd.read_excel(cdil_code, sheet_name = 'data', skiprows = range(1,3,1), nrows = 3, header = [0])

df.drop('Sample Submission ID/Lab ID', inplace=True, axis=1)
df.drop('SL', inplace=True, axis=1)
df.drop('Unnamed: 21', inplace=True, axis=1)

datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/cdilcode.csv') #checking if skiprows and header give the desired result


ast_data = pd.melt(df,id_vars=df.columns[3:], value_vars=df.columns[0:19],var_name='antibiotic', value_name='sensitivity')

ast_data.to_csv(f'{datacheck}/cdilmelt.csv')

