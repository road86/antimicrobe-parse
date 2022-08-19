import pandas as pd
import os
import uuid

data_file = os.path.join('..','input_data','unsorted','AST data_ready to use','Khulna medical College_Jan 2021-Jul 2022-PATIENT_NAMES_REMOVED.xlsx')

df = pd.read_excel(data_file, header=[0,1,2])
corrected_cols = [x[1] for x in df.columns[0:7]] + [x[2] for x in df.columns[7:]]
df.columns = corrected_cols

df.insert(0,'amr_uuid', [uuid.uuid4() for _ in range(len(df.index))])

ast_data = pd.melt(df,id_vars=df.columns[0:12], value_vars=df.columns[12:-3],var_name='antibiotic', value_name='sensitivity')

#there are two identical columns for each antibiotic, one has MIC result, another an interpretation
# we can get MIC from here later on

ast_data = ast_data[['amr_uuid','Sl no', 'Date of enrollment', 'Age',
       'Specimen type', 'Identified bacteria',
       'antibiotic', 'sensitivity']]

ast_data.columns = ['amr_uuid','lab_id', 'sample_date','sample_age', 'specimen', 'pathogen', 'antibiotic', 'sensitivity']

ast_data = ast_data[ast_data['sensitivity'].isin(['S','R','I','s'])]

nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'khulna-mc'
location_name = 'khulna'

ast_data['location']=pd.Series(location_name,index=ast_data.index)
ast_data['provider']=pd.Series(provider_name,index=ast_data.index)


print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')

ast_data.to_csv(os.path.join('outdata',f'ast_data_khulna-mc.csv'))
