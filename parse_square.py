import uuid
import pandas as pd
import os

square_data = os.path.join('..','input_data','unsorted','AST data_ready to use','Sq AST 2018.sav')
df = pd.read_spss(square_data)
df.insert(0,'amr_uuid', [uuid.uuid4() for _ in range(len(df.index))])

#Instead of iterating through each row we can melt this wide format data into long format data.

ast_data = pd.melt(df,id_vars=df.columns[0:6], value_vars=df.columns[6:-2],var_name='antibiotic', value_name='sensitivity')

ast_data = ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample
ast_data = ast_data.reset_index()
ast_data = ast_data[['index','amr_uuid','sex','Age','Specimen','Organism','antibiotic','sensitivity']]

ast_data.columns = ['lab_id','amr_uuid', 'sample_sex', 'sample_age', 'specimen', 'pathogen', 'antibiotic', 'sensitivity']


ast_data['sample_date']=pd.Series('2021',index=ast_data.index)


nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'square'
location_name = 'dhaka'

ast_data['location']=pd.Series(location_name,index=ast_data.index)
ast_data['provider']=pd.Series(provider_name,index=ast_data.index)


print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')


ast_data.to_csv(os.path.join('outdata','ast_data_square.csv'))
