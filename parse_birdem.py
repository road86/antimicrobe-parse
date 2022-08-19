import re
import pandas as pd
import os
import uuid

birdem_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'BIRDEM Hospital_2021.xlsx')

df = pd.read_excel(birdem_data)

df.insert(0,'amr_uuid', [uuid.uuid4() for _ in range(len(df.index))])
megagigalist = []

#for each antibiotic result there is a columns
range_abio_columns = range(23, len(df.columns))

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'amr_uuid':rrr['amr_uuid'],
            'lab_id': rrr['Lab ID'],
            'sample_sex': rrr['Gender'],
            'sample_age': rrr['Age'],
            'sample_date': rrr['MR Receiving Date'],
            'specimen': rrr['Sample Name'],
            'pathogen': rrr['Organism Name'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]
        }
        if rrr['Observation'] != 'No Growth':
             megagigalist.append(new_df)

outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data = ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample

nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'birdem'
location_name = 'dhaka'

ast_data['location']=pd.Series(location_name,index=ast_data.index)
ast_data['provider']=pd.Series(provider_name,index=ast_data.index)


print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')


ast_data.to_csv(f'{outputloc}/ast_data_birdem.csv')
