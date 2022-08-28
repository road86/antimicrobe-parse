import re
import pandas as pd
import os
import numpy as np
import uuid

cdil_data = os.path.join('..','input_data', 'unsorted', 'Animal Health data', 'AST-Results_analysis (CDIL).xlsx')

df = pd.read_excel(cdil_data, sheet_name = 'data', skiprows = range(1,6,1), header = [0])
df.insert(loc=1, column='pathogen', value='Escherichia coli', allow_duplicates=True)
df.insert(0,'amr_uuid', [uuid.uuid4() for _ in range(len(df.index))])

#checking
datacheck = 'check' # folder to store script checks
df.to_csv(f'{datacheck}/cdil.csv') #checking if skiprows and header give the desired result

megagigalist = []


ast_data = pd.melt(df,id_vars=df.columns[0:6], value_vars=df.columns[6:-1],var_name='antibiotic', value_name='mic')


ast_data.columns = ['amr_uuid', 'SL', 'pathogen', 'lab_id','Unnamed: 2', 'AMP', 'antibiotic', 'mic']
ast_data = ast_data[['amr_uuid', 'pathogen', 'lab_id','antibiotic', 'mic']]

#interpretation of MIC results

df2 = pd.read_excel(cdil_data, sheet_name = 'data', skiprows = range(1,3,1), nrows = 3, header = [0])

df2.drop('Sample Submission ID/Lab ID', inplace=True, axis=1)
df2.drop('SL', inplace=True, axis=1)
df2.drop('Unnamed: 21', inplace=True, axis=1)


thresh = df2.set_index('Unnamed: 2').T

ast_data['mic'] = pd.to_numeric(ast_data['mic'],errors='coerce')
ast_data = ast_data.dropna(subset=['mic'])
ast_data['sensitivity'] = ast_data.apply(lambda x: 'S' if x['mic'] >= thresh.loc[x['antibiotic']]['CLSI S >='] else 'R' if x['mic'] <= thresh.loc[x['antibiotic']]['CLSI R<='] else 'I', axis = 1)

nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'cdil'
location_name = 'dhaka'

ast_data['location']=pd.Series(location_name,index=ast_data.index)
ast_data['provider']=pd.Series(provider_name,index=ast_data.index)


print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')

ast_data.to_csv(os.path.join('outdata',f'ast_poultry_cdil.csv'))
