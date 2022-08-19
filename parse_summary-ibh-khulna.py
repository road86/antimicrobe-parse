import re
import pandas as pd
import os

ibhkhulna_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'Islami Bank Hospital, Khulna_Jul 2021-Jun 2022 (1).xlsx')

df_urine = pd.read_excel(ibhkhulna_data, sheet_name = 'Urine', skiprows = 1, header = [2])
df_nipple = pd.read_excel(ibhkhulna_data, sheet_name = 'Nipple Swab', skiprows = 0, header = [1])
df_pus = pd.read_excel(ibhkhulna_data, sheet_name = 'Pus', skiprows = 0, header = [1])
df_wound = pd.read_excel(ibhkhulna_data, sheet_name = 'Wound Swab', skiprows = 0, header = [1])
df_stool = pd.read_excel(ibhkhulna_data, sheet_name = 'Stool', skiprows = 0, header = [1])

os.makedirs('check') # will return error if file exists
datacheck = 'check' 
## Checks
df_urine.to_csv(f'{datacheck}/check_urine.csv')
df_nipple.to_csv(f'{datacheck}/check_nipple.csv')
df_pus.to_csv(f'{datacheck}/check_pus.csv')
df_wound.to_csv(f'{datacheck}/check_wound.csv')
df_stool.to_csv(f'{datacheck}/check_stool.csv')
########## Checks over

megagigalist = []

range_abio_urine = range(2, len(df_urine.columns))
range_abio_nipple = range(2, len(df_nipple.columns))
range_abio_pus = range(2, len(df_pus.columns))
range_abio_wound = range(2, len(df_wound.columns))
range_abio_stool = range(2, len(df_stool.columns))

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

#for Nipple
for iii, rrr in df_nipple.iterrows():
    for abioind2 in range_abio_nipple:
        nipple_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind2],
            'sensitive_isolates': rrr[rrr.index[abioind2]]
        }
        nipple_df['specimen']='Nipple Swab'
        megagigalist.append(nipple_df)

# for pus
for iii, rrr in df_pus.iterrows():
    for abioind3 in range_abio_pus:
        pus_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind3],
            'sensitive_isolates': rrr[rrr.index[abioind3]]
        }
        pus_df['specimen']='Pus'
        megagigalist.append(pus_df)

# for wound
for iii, rrr in df_wound.iterrows():
    for abioind4 in range_abio_wound:
        wound_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind4],
            'sensitive_isolates': rrr[rrr.index[abioind4]]
        }
        wound_df['specimen']='Wound Swab'
        megagigalist.append(wound_df)

# for stool
for iii, rrr in df_stool.iterrows():
    for abioind5 in range_abio_stool:
        stool_df = {
            'pathogen': rrr['Organism'],
            'isolates_number': rrr['Number of isolates'],
            'antibiotic': rrr.index[abioind5],
            'sensitive_isolates': rrr[rrr.index[abioind5]]
        }
        stool_df['specimen']='Stool'
        megagigalist.append(stool_df)


outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data['sensitivity']=ast_data['sensitive_isolates']/ast_data['isolates_number']
ast_data['location']=pd.Series('khulna',index=ast_data.index)
ast_data['provider']=pd.Series('islamic bank hospital',index=ast_data.index)

ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample


ast_data.to_csv(f'{outputloc}/ast_data_ibhkhulna.csv')