import re
import pandas as pd
import os

rabeya_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'Jalalabag Ragib-Rabeya Med Col_Aug 20, 2022 (1).xlsx')

df_urine = pd.read_excel(rabeya_data, sheet_name = 'Urine', skiprows = 1, header = [2])
df_pus = pd.read_excel(rabeya_data, sheet_name = 'Pus', skiprows = 0, header = [1])
df_wound = pd.read_excel(rabeya_data, sheet_name = 'Wound Swab', skiprows = 0, header = [1])
df_stool = pd.read_excel(rabeya_data, sheet_name = 'Stool', skiprows = 0, header = [1])
df_blood = pd.read_excel(rabeya_data, sheet_name = 'Blood', skiprows = 0, header = [1])
df_sputum = pd.read_excel(rabeya_data, sheet_name = 'Sputum', skiprows = 0, header = [1])

os.makedirs('check') # will return error if file exists
datacheck = 'check' 
## Checks
df_urine.to_csv(f'{datacheck}/check_uriner.csv')
df_pus.to_csv(f'{datacheck}/check_pusr.csv')
df_wound.to_csv(f'{datacheck}/check_woundr.csv')
df_stool.to_csv(f'{datacheck}/check_stoolr.csv')
df_blood.to_csv(f'{datacheck}/check_bloodr.csv')
df_sputum.to_csv(f'{datacheck}/check_sputumr.csv')

########## Checks over

megagigalist = []

range_abio_urine = range(2, len(df_urine.columns))
range_abio_pus = range(2, len(df_pus.columns))
range_abio_wound = range(2, len(df_wound.columns))
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

# for Pus
for iii, rrr in df_pus.iterrows():
    for abioind2 in range_abio_pus:
        pus_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind2],
            'sensitive_isolates': rrr[rrr.index[abioind2]]
        }
        pus_df['specimen']='Pus'
        megagigalist.append(pus_df)

# for Wound
for iii, rrr in df_wound.iterrows():
    for abioind3 in range_abio_wound:
        wound_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind3],
            'sensitive_isolates': rrr[rrr.index[abioind3]]
        }
        wound_df['specimen']='Wound Swab'
        megagigalist.append(wound_df)

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

# High Blood
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
ast_data['location']=pd.Series('sylhet',index=ast_data.index)
ast_data['provider']=pd.Series('jalalabad ragib rabeya medical college',index=ast_data.index)

ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample


ast_data.to_csv(f'{outputloc}/ast_data_ragib_rabeya_mc.csv')