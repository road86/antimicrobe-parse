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
ast_data['sensitivity'] = ast_data.apply(lambda x: 's' if x['mic'] >= thresh.loc[x['antibiotic']]['CLSI S >='] else 'r' if x['mic'] <= thresh.loc[x['antibiotic']]['CLSI R<='] else 'i', axis = 1)

nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'CDIL'
location_name = 'dhaka'



print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')

prepdata = ast_data.groupby(['pathogen','antibiotic','sensitivity'])['amr_uuid'].count().reset_index()

ast_poultry = pd.pivot(prepdata, index=['pathogen','antibiotic'], columns='sensitivity', values='amr_uuid').reset_index()

ast_poultry.columns = ['pathogen', 'antibiotic', 'count_i', 'count_r', 'count_s']

ast_poultry = ast_poultry.fillna(0)
ast_poultry['total'] = ast_poultry[list(ast_poultry.columns[2:])].sum(axis=1)

ast_poultry['sensitive_isolates'] = ast_poultry['count_s']
ast_poultry['sensitivity'] = ast_poultry.apply(lambda x: x['count_s']/(x['total']),axis=1)

niso = ast_data.groupby(['pathogen'])['amr_uuid'].nunique().reset_index().iloc[0]['amr_uuid']
ast_poultry = ast_poultry[['pathogen', 'antibiotic','sensitive_isolates', 'sensitivity']]
ast_poultry['isolates_number']=pd.Series(niso,index=ast_poultry.index)
ast_poultry['location']=pd.Series(location_name,index=ast_poultry.index)
ast_poultry['provider']=pd.Series(provider_name,index=ast_poultry.index)

ast_poultry.to_csv(os.path.join('outdata',f'ast_poultry_cdil.csv'))
