import pandas as pd
import os
import amr_utils


preprocessed_animal_files = ['ast_poultry_aftab.csv','ast_poultry_BARC.csv' , 'ast_poultry_nourish.csv']

indata_dir = 'outdata'
list_of_dfs = []
for ppf in preprocessed_animal_files:
    ast_data_part = pd.read_csv(os.path.join(indata_dir,ppf))
    list_of_dfs.append(ast_data_part)

ast_data_animal = pd.concat(list_of_dfs)


ast_data_animal_preclean = amr_utils.clean(ast_data_animal, summary=True, animal=True)

ast_data_animal_preclean.to_csv(os.path.join('outdata','ast_data_animal_clean.csv'))
