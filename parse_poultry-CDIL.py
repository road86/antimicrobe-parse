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

#for each antibiotic result there is a columns
range_abio_columns = range(6, len(df.columns))

for iii, rrr in df.iterrows():
    for abioind in range_abio_columns:
        new_df = {
            'amr_uuid':rrr['amr_uuid'],
            'lab_id': rrr['Sample Submission ID/Lab ID'],
            'specimen': rrr['Sample Name'],
            'pathogen': rrr['pathogen'],
            'antibiotic': rrr.index[abioind],
            'sensitivity': rrr[rrr.index[abioind]]
        }

