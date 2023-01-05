import re
import pandas as pd
import os
import uuid


epic_data = os.path.join('..', 'input_data', '20-21-22-chittagong-epic', '01.01.22 to 23.09.22_cleaned_wuz.xlsx')

df = pd.read_excel(epic_data, header=[0])
#corrected_cols = [x[0] for x in df.columns[0:4]] + [x[1] for x in df.columns[4:]]
#df.columns = corrected_cols
df.insert(0,'amr_uuid', [uuid.uuid4() for _ in range(len(df.index))])
range_abio_columns = range(5, len(df.columns))

megagigalist = []


for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'amr_uuid': rrr['amr_uuid'],
            'sample_sex': rrr['Patient Name'].split(',')[0],
            'sample_age': rrr['Patient Name'].split(',')[1],
            'specimen':rrr['Specimen Type'],
            'pathogen':rrr['Organism Name'],
            'antibiotic':rrr.index[abioind],
            'sensitivity':rrr[rrr.index[abioind]]
            }
        megagigalist.append(new_df)

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data =  ast_data.dropna(subset=['sensitivity'])

outputloc = "outdata"

nisolates = len(ast_data['amr_uuid'].unique())
nrecords = len(ast_data['amr_uuid'])
nantiperiso = nrecords/nisolates
provider_name = 'epic'
location_name = 'chittagong'

ast_data['location']=pd.Series(location_name,index=ast_data.index)
ast_data['provider']=pd.Series(provider_name,index=ast_data.index)

print(f'Provider {provider_name} from {location_name} has {nisolates} isolates of bacteria with a total of {nrecords} antibiotic sensitivity tested, which is {nantiperiso:.2f} antibiotics tested per isolate')


ast_data.to_csv(f'{outputloc}/ast_data_epic.csv')
