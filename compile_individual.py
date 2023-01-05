import pandas as pd
import re
import os
import uuid
import amr_utils

#read in ast data parsed from various providers.
preprocessed_files = ['ast_data_chevron.csv', 'ast_data_epic.csv', 'ast_data_birdem.csv','ast_data_adhumic.csv','ast_data_square.csv','ast_data_imperial.csv','ast_data_khulna-mc.csv']
indata_dir = 'outdata'

if os.getenv('AMR_TEST') == 'test':
    preprocessed_files = ['ast_data_test.csv']
    indata_dir = 'test'

list_of_dfs = []
for ppf in preprocessed_files:
    ast_data_part = pd.read_csv(os.path.join(indata_dir,ppf))
    list_of_dfs.append(ast_data_part)

ast_data = pd.concat(list_of_dfs)

ast_data_preclean = amr_utils.clean(ast_data)

ast_data_preclean.to_csv(os.path.join('outdata','ast_data_clean.csv'))
