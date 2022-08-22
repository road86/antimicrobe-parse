import re
import pandas as pd
import os

mos_data = os.path.join('..','input_data', 'unsorted', 'Data Updating', 'Chattogram Ma O Shishu Hospital_2021 (1).xlsx')

print(f'Not working yet input file missing: {mos_data}')
exit(0)

df_urine = pd.read_excel(mos_data, sheet_name = 'Urine', skiprows = 1, header = [2])
df_wound = pd.read_excel(mos_data, sheet_name = 'Wound', skiprows = 0, header = [1])
df_trachea = pd.read_excel(mos_data, sheet_name = 'Tracheal Aspirate', skiprows = 0, header = [1])
df_stool = pd.read_excel(mos_data, sheet_name = 'Stool', skiprows = 0, header = [1])
df_blood = pd.read_excel(mos_data, sheet_name = 'Blood', skiprows = 0, header = [1])
df_sputum = pd.read_excel(mos_data, sheet_name = 'Sputum', skiprows = 0, header = [1])

os.makedirs('check') # will return error if file exists
datacheck = 'check'
## Checks
df_urine.to_csv(f'{datacheck}/check_urinemos.csv')
df_wound.to_csv(f'{datacheck}/check_woundmos.csv')
df_trachea.to_csv(f'{datacheck}/check_tracheamos.csv')
df_stool.to_csv(f'{datacheck}/check_stoolmos.csv')
df_blood.to_csv(f'{datacheck}/check_bloodmos.csv')
df_sputum.to_csv(f'{datacheck}/check_sputummos.csv')

########## Checks over

megagigalist = []

range_abio_urine = range(2, len(df_urine.columns))
range_abio_wound = range(2, len(df_wound.columns))
range_abio_trachea = range(2, len(df_trachea.columns))
range_abio_stool = range(2, len(df_stool.columns))
range_abio_blood = range(2, len(df_blood.columns))
range_abio_sputum = range(2, len(df_sputum.columns))

# for Urine
for iii, rrr in df_urine.iterrows():
    for abioind1 in range_abio_urine:
        urine_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind1],
            'sensitive_isolates': rrr[rrr.index[abioind1]]
        }
        urine_df['specimen']='Urine'
        megagigalist.append(urine_df)

# for Wound
for iii, rrr in df_wound.iterrows():
    for abioind2 in range_abio_wound:
        wound_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind2],
            'sensitive_isolates': rrr[rrr.index[abioind2]]
        }
        wound_df['specimen']='Wound'
        megagigalist.append(wound_df)

# for Tracheal Aspirate
for iii, rrr in df_trachea.iterrows():
    for abioind3 in range_abio_trachea:
        trachea_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind3],
            'sensitive_isolates': rrr[rrr.index[abioind3]]
        }
        trachea_df['specimen']='Tracheal Aspirate'
        megagigalist.append(trachea_df)

# for Stool
for iii, rrr in df_stool.iterrows():
    for abioind4 in range_abio_stool:
        stool_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind4],
            'sensitive_isolates': rrr[rrr.index[abioind4]]
        }
        stool_df['specimen']='Stool'
        megagigalist.append(stool_df)

# Blood
for iii, rrr in df_blood.iterrows():
    for abioind5 in range_abio_blood:
        blood_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind5],
            'sensitive_isolates': rrr[rrr.index[abioind5]]
        }
        blood_df['specimen']='Blood'
        megagigalist.append(blood_df)

# for Sputum
for iii, rrr in df_sputum.iterrows():
    for abioind6 in range_abio_sputum:
        sputum_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind6],
            'sensitive_isolates': rrr[rrr.index[abioind6]]
        }
        sputum_df['specimen']='Sputum'
        megagigalist.append(sputum_df)

outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data['sensitivity']=ast_data['sensitive_isolates']/ast_data['isolates_number']
ast_data['location']=pd.Series('chittagong',index=ast_data.index)
ast_data['provider']=pd.Series('maa o shishu hospital',index=ast_data.index)

ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample


ast_data.to_csv(f'{outputloc}/ast_data_maa_o_shishu.csv')
