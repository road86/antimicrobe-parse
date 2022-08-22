import re
import pandas as pd
import os

akij_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'AD-din Akij Medical College, Khulna_Jun 2021-Aug 2022_ok (1).xlsx')

df_blood = pd.read_excel(akij_data, sheet_name = 'Blood', skiprows = 1, header = [2])
df_urine = pd.read_excel(akij_data, sheet_name = 'Urine', skiprows = 0, header = [1])
df_pus = pd.read_excel(akij_data, sheet_name = 'Pus', skiprows = 0, header = [1])
df_stool = pd.read_excel(akij_data, sheet_name = 'Stool', skiprows = 0, header = [1])

os.makedirs('check', exist_ok=True)
datacheck = 'check'
## Checks
df_blood.to_csv(f'{datacheck}/check_blood_akij.csv')
df_urine.to_csv(f'{datacheck}/check_urine_akij.csv')
df_pus.to_csv(f'{datacheck}/check_pus_akij.csv')
df_stool.to_csv(f'{datacheck}/check_stool_akij.csv')
########## Checks over

megagigalist = []

range_abio_blood = range(2, len(df_blood.columns))
range_abio_urine = range(2, len(df_urine.columns))
range_abio_pus = range(2, len(df_pus.columns))
range_abio_stool = range(2, len(df_stool.columns))

# for Blood
for iii, rrr in df_blood.iterrows():
    for abioind1 in range_abio_blood:
        blood_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind1],
            'sensitive_isolates': rrr[rrr.index[abioind1]]
        }
        blood_df['specimen'] = 'Blood'
        megagigalist.append(blood_df)

# for Urine
for iii, rrr in df_urine.iterrows():
    for abioind2 in range_abio_urine:
        urine_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind2],
            'sensitive_isolates': rrr[rrr.index[abioind2]]
        }
        urine_df['specimen'] = 'Urine'
        megagigalist.append(urine_df)

# for Pus
for iii, rrr in df_pus.iterrows():
    for abioind3 in range_abio_pus:
        pus_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind3],
            'sensitive_isolates': rrr[rrr.index[abioind3]]
        }
        pus_df['specimen'] = 'Pus'
        megagigalist.append(pus_df)

# for Stool
for iii, rrr in df_stool.iterrows():
    for abioind4 in range_abio_stool:
        stool_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind4],
            'sensitive_isolates': rrr[rrr.index[abioind4]]
        }
        stool_df['specimen'] = 'Stool'
        megagigalist.append(stool_df)

outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data['sensitivity']=ast_data['sensitive_isolates']/ast_data['isolates_number']
ast_data['location']=pd.Series('khulna',index=ast_data.index)
ast_data['provider']=pd.Series('ad-din akij medical college',index=ast_data.index)

ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample


ast_data.to_csv(f'{outputloc}/ast_data_akij.csv')
