import re
import pandas as pd
import os

bbaria_data = os.path.join('..','input_data', 'unsorted', 'AST data_ready to use', 'Brammanbaria medical college_B.Baria_Aug 2022.xlsx')

df_urine = pd.read_excel(bbaria_data, sheet_name = 'Urine', skiprows = 1, header = [2])


os.makedirs('check', exist_ok=True)
datacheck = 'check'
## Check
df_urine.to_csv(f'{datacheck}/check_urinebbaria.csv')
########## Check over

megagigalist = []

range_abio_urine = range(2, len(df_urine.columns))



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



outputloc = "outdata"

ast_data = pd.DataFrame.from_records(megagigalist)
ast_data['sensitivity']=ast_data['sensitive_isolates']/ast_data['isolates_number']
ast_data['location']=pd.Series('Brahmanbaria',index=ast_data.index)
ast_data['provider']=pd.Series('Brahmanbaria Medical College',index=ast_data.index)

ast_data =  ast_data.dropna(subset=['sensitivity']) #remove many datapoints for antibiotics not tested for each sample


ast_data.to_csv(f'{outputloc}/ast_data_bbaria_mc.csv')