import pandas as pd
import os
import amr_utils


preprocessed_summary_files = ['ast_data_akij.csv','ast_data_ragib_rabeya_mc.csv','ast_data_popular_diagnostic_rangpur.csv','ast_data_ibhdhaka.csv','ast_data_ibhkhulna.csv','ast_data_ibhbarisal.csv', 'ast_data_maa_o_shishu.csv', 'ast_data_ibhrajshahi.csv']

indata_dir = 'outdata'
list_of_dfs = []
for ppf in preprocessed_summary_files:
    ast_data_part = pd.read_csv(os.path.join(indata_dir,ppf))
    list_of_dfs.append(ast_data_part)

ast_data_summary = pd.concat(list_of_dfs)


ast_data_summary_preclean = amr_utils.clean(ast_data_summary, summary=True)

ast_data_summary_preclean.to_csv(os.path.join('outdata','ast_data_summary_clean.csv'))
