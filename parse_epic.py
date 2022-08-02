import pandas as pd

epic_file = 'input_data/20-chittagong-epic/22-12-20 Epic (1).xlsx'

df = pd.read_excel(epic_file)
megagigalist = []


for iii, rrr in df.iterrows():
    for abioind in range(84,122):
        new_df = {
            'lab_id': rrr['Lab ID'],
            'sample_sex': rrr['Patient Name'].split(',')[0],
            'sample_age': rrr['Patient Name'].split(',')[1],
            'patient_id': rrr['Patient ID'],
            'specimen':rrr['Specimen Type'],
            'pathogen':rrr['Organism Name'],
            'card_type':rrr['Card Type'],
            'antibiotic':rrr.index[abioind],
            'mic':rrr[rrr.index[abioind]]
            }
        megagigalist.append(new_df)

ast_data_epic = pd.DataFrame.from_records(megagigalist)
ast_data_epic.to_csv(f'{outputloc}/ast_data_epic.csv')
